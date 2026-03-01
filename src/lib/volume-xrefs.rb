# AW: I used Gemini to write this script.  Here's the session-resume prompt:

# Session Resume: Asciidoctor Cross-Volume Xref Extension
# The Goal: Automatically format <<anchor>> as "Volume I, Chapter 2" or "Chapter 2" based on volume boundaries in a 1,000+ page book.
# Technical Breakthroughs:
# Memory: Switched from find_by (which returns a giant array and triggers SIGKILL) to an Iterative Visitor that returns false to discard processed blocks immediately.
# Speed: Eliminated .source calls (which re-serialize the AST) and manual recursion (which hit infinite loops). Used In-place Mutation (lines[i] = ...) to avoid Ruby object churn.
# Logic: Implemented a Parent Volume Cache to stop redundant tree-climbing for the 10,000+ nodes in the document.
# The Production Script:


require 'asciidoctor'
require 'asciidoctor/extensions'

Asciidoctor::Extensions.register do
  treeprocessor do
    process do |doc|
      # 1. INDEXING (Keep as is, it works fine)
      vol_map, parent_vol_cache = {}, {}
      doc.catalog[:refs].each do |id, ref|
        next unless ref.is_a?(Asciidoctor::Section)
        target_vol, curr = "unknown", ref
        while curr && curr != doc
          if parent_vol_cache[curr.object_id]
            target_vol = parent_vol_cache[curr.object_id]; break
          elsif curr.attributes.key?('volume')
            target_vol = curr.attr('volume').to_s.upcase
            parent_vol_cache[curr.object_id] = target_vol; break
          end
          curr = curr.parent
        end
        label = ref.special ? "Appendix" : (ref.level == 1 ? "Chapter" : "Section")
        num = ref.respond_to?(:sectnum) ? ref.sectnum.to_s.chomp('.') : id
        vol_map[id] = { vol: target_vol, label: label, num: num }
      end

      xref_re = /<<([^,>]+)>>/

      # 2. UPDATED ITERATIVE VISITOR (Uses raw variables to avoid conversion crashes)
      doc.find_by do |block|
        # Use instance variables to check for text without triggering 'convert'
        raw_lines = block.instance_variable_get(:@lines)
        raw_text = block.instance_variable_get(:@text)

        if (raw_lines && !raw_lines.empty?) || (raw_text && raw_text.include?('<<'))
          current_vol, curr = "unknown", block
          while curr && curr != doc
            (current_vol = curr.attr('volume').to_s.upcase; break) if curr.attributes.key?('volume')
            curr = curr.parent
          end

          processor = lambda do |text|
            text.gsub(xref_re) do |match|
              if (data = vol_map[$1])
                lbl = (data[:vol] != current_vol) ? "Volume #{data[:vol]}, #{data[:label]} #{data[:num]}" : "#{data[:label]} #{data[:num]}"
                "<<#{$1},#{lbl}>>"
              else; match; end
            end
          end

          # Modify raw lines or text directly
          if raw_lines
            raw_lines.each_with_index { |l, i| raw_lines[i] = processor.call(l) if l.include?('<<') }
          elsif raw_text
            block.instance_variable_set(:@text, processor.call(raw_text))
          end
        end
        false
      end
      doc
    end
  end
end
