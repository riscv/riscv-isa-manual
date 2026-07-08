# changebar.rb — automatic git-driven changebars for the RISC-V PDF build.
#
# Marks the left margin of every block whose source lines differ between a base
# ref and the working tree, so a reader can see exactly what a branch changed
# without any manual annotation.
#
# It has two halves:
#
#   1. A tree processor that reads a JSON map of changed line ranges (produced by
#      scripts/gen-changebar-diff.sh) and, using Asciidoctor's sourcemap, adds
#      the "changed" role to each affected block.
#   2. A PDF converter that draws a vertical bar in the left margin next to any
#      block carrying that role.
#
# Enable it in a build with:
#   asciidoctor-pdf --sourcemap -r ./src/lib/changebar.rb \
#     -a changebar-diff=<path-to-changes.json> ...
#
# With no changebar-diff attribute (or an empty map) it is a complete no-op, so
# it is safe to leave wired into a build target.
#
# NOTE: the converter half depends on a few asciidoctor-pdf internals
# (ink_general_heading / ink_chapter_title / ink_part_title and the section's
# pdf-page-start attribute). The build pins asciidoctor-pdf via the docs base
# container image, so these are stable for this repo; revisit on a major bump.

require 'json'
require 'asciidoctor-pdf'

module Changebar
  ROLE = 'changed'.freeze

  # Barable = block contexts the converter knows how to draw a bar around. When
  # a changed line lands in a finer node (a list item, a table cell) we climb to
  # the nearest ancestor in this set.
  BARABLE = %i[
    section paragraph listing literal ulist olist dlist admonition quote
    example sidebar open verse image table thematic_break floating_title pass
  ].freeze

  # Normalise a source path to a repo-relative "src/..." key so paths from git
  # (repo-relative) and from Asciidoctor's sourcemap (absolute, and different
  # inside the build container) compare equal.
  def self.normalize(path)
    return nil unless path
    if (i = path.rindex('/src/'))
      path[(i + 1)..]
    elsif path.start_with?('src/')
      path
    else
      File.basename(path)
    end
  end

  # Load { "src/foo.adoc" => [[start,end], ...] } from the JSON file named by the
  # changebar-diff attribute. Returns {} when unset or unreadable.
  def self.load_ranges(doc)
    spec = doc.attr('changebar-diff')
    return {} if spec.nil? || spec.empty?
    # Resolve against the document base dir, then the working dir, then as given
    # — base_dir differs between a local build and the container build.
    candidates = [spec, File.expand_path(spec, Dir.pwd)]
    candidates << (doc.normalize_system_path(spec, doc.base_dir) rescue nil)
    path = candidates.compact.find { |c| File.file?(c) }
    return {} unless path
    raw = JSON.parse(File.read(path))
    raw.each_with_object({}) do |(file, ranges), acc|
      acc[normalize(file)] = ranges.map { |a, b| [a.to_i, b.to_i] }
    end
  rescue JSON::ParserError
    {}
  end
end

# ---------------------------------------------------------------------------
# Tree processor: tag changed blocks.
# ---------------------------------------------------------------------------
Asciidoctor::Extensions.register do
  tree_processor do
    process do |doc|
      ranges = Changebar.load_ranges(doc)
      next if ranges.empty?

      # Collect barable blocks with a known source location, grouped by file.
      by_file = Hash.new { |h, k| h[k] = [] }
      doc.find_by.each do |node|
        next unless Changebar::BARABLE.include?(node.context)
        sl = node.source_location rescue nil
        next unless sl && sl.file && sl.lineno
        key = Changebar.normalize(sl.file)
        by_file[key] << [sl.lineno, node]
      end

      by_file.each do |file, entries|
        file_ranges = ranges[file]
        next unless file_ranges

        entries.sort_by! { |lineno, _| lineno }
        starts = entries.map(&:first)

        entries.each_with_index do |(lineno, node), idx|
          # A block "owns" the lines from its start up to the next barable
          # block's start; mark it if any changed line falls in that span.
          span_end = idx + 1 < starts.length ? starts[idx + 1] - 1 : Float::INFINITY
          changed = file_ranges.any? do |lo, hi|
            lo <= span_end && hi >= lineno
          end
          node.add_role(Changebar::ROLE) if changed
        end
      end
      nil
    end
  end
end

# ---------------------------------------------------------------------------
# Converter: draw the bars.
# ---------------------------------------------------------------------------
class ChangebarConverter < (Asciidoctor::Converter.for 'pdf')
  register_for 'pdf'

  BAR_COLOR = 'D64541'.freeze
  BAR_WIDTH = 2.5
  BAR_INSET = 12 # points left of the content box
  BAR_PAD   = 5  # extend each bar so adjacent changed blocks merge visually

  # Sections draw a bar around the heading only; their changed descendants are
  # marked and barred individually. This keeps a one-line edit inside a big
  # section from barring the whole section, while a wholly-new section still
  # reads as a continuous bar (heading + every child block).
  def convert_section(node, opts = {})
    return super unless changed?(node)
    prev = @cb_active_section
    @cb_active_section = node
    super
    region = (@cb_regions ||= {}).delete(node.object_id)
    draw_region(region) if region
    @cb_active_section = prev
  end

  # Capture the heading's rendered extent (after any chapter page break) so the
  # section bar hugs the title exactly. Keyed per node so nested changed
  # sections don't clobber each other's region.
  %i[ink_general_heading ink_chapter_title ink_part_title].each do |m|
    define_method(m) do |*args, &blk|
      node = args.first
      unless node.equal?(@cb_active_section)
        return super(*args, &blk)
      end
      start_page = page_number
      start_top = cursor
      result = super(*args, &blk)
      (@cb_regions ||= {})[node.object_id] =
        { start_page: start_page, start_top: start_top,
          end_page: page_number, end_bottom: cursor }
      result
    end
  end

  %i[paragraph listing literal ulist olist dlist admonition quote
     example sidebar open verse image table thematic_break].each do |ctx|
    define_method(:"convert_#{ctx}") do |node, *rest|
      unless changed?(node) && !ancestor_changed?(node)
        return super(node, *rest)
      end
      start_page = page_number
      start_top = cursor
      result = super(node, *rest)
      # draw_region restores the text cursor to the post-block position itself.
      draw_region(start_page: start_page, start_top: start_top,
                  end_page: page_number, end_bottom: cursor)
      result
    end
  end

  private

  def changed?(node)
    node.respond_to?(:role?) && node.role? && node.roles.include?(Changebar::ROLE)
  end

  # Avoid a doubled bar when a changed block sits inside an already-barred
  # ancestor (e.g. a changed list inside a changed open block).
  def ancestor_changed?(node)
    p = node.parent
    while p
      if p.respond_to?(:roles) && p.respond_to?(:role?) && p.role? &&
         p.roles.include?(Changebar::ROLE) && p.context != :section
        return true
      end
      p = p.respond_to?(:parent) ? p.parent : nil
    end
    false
  end

  # Stroke the bar across every page the region spans, then restore the text
  # cursor (go_to_page resets it to the page top, which would corrupt the flow).
  def draw_region(region)
    start_page = region[:start_page]
    end_page   = region[:end_page]
    start_top  = region[:start_top]
    end_bottom = region[:end_bottom]
    resume_page = page_number
    resume_cursor = cursor
    bar_x = bounds.left - BAR_INSET

    (start_page..end_page).each do |pnum|
      go_to_page pnum
      top    = pnum == start_page ? [start_top + BAR_PAD, bounds.height].min : bounds.height
      bottom = pnum == end_page   ? [end_bottom - BAR_PAD, 0].max : 0
      next if top <= bottom
      stroke do
        line_width BAR_WIDTH
        stroke_color BAR_COLOR
        stroke_vertical_line bottom, top, at: bar_x
      end
    end

    go_to_page resume_page
    move_cursor_to resume_cursor
  end
end
