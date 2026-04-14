require 'asciidoctor'
require 'asciidoctor/extensions'

# Macro                   Expands to
#
# insn:foo[]              FOO
# insn:foo[bar,baz]       FOO bar, baz
#
# insnlink:foo[]          <<insn:foo, FOO>>
# insnlink:foo[bar,baz]   <<insn:foo, FOO bar, baz>>
#
# ext:zoo[]               `Zoo`
#
# extlink:zoo[]           <<ext:zoo, `Zoo`>>
#
# csr:foo[]               `foo`
# csr::[bar]              `BAR`
# csr:foo[bar]            `foo.BAR`
#
# csrlink:foo[]           <<csr:foo, `foo`>>
# csrlink:foo[bar]        <<csr:foo_bar, `foo.BAR`>>

module RVFormat
  def self.instruction(name, args)
    name.upcase + (args.any? ? "\u{a0}" : "") + args.values.join(",\u{a0}")
  end

  def self.extension(name)
    "`#{name.capitalize}`"
  end

  def self.csr(name, field)
    name = name.empty? ? [] : [name.downcase]
    field = field.empty? ? [] : [field.upcase]
    "`#{(name + field).join(".\u{2060}")}`"
  end

  def self.process(processor, parent, name)
    processor.create_inline parent, :quoted, parent.apply_subs(name, [:quotes])
  end

  def self.process_xref(processor, parent, name, ref)
    # Record references for subsequent invalid reference detection
    (parent.document.attributes['RVFormat.xrefs'] ||= []) << ref

    processor.create_inline parent, :anchor, "#{name}", type: :xref, target: "##{ref}", attributes: { 'subs' => :normal }
  end
end

Asciidoctor::Extensions.register do
  inline_macro :insn do
    process do |parent, name, args|
      RVFormat.process(self, parent, RVFormat.instruction(name, args))
    end
  end

  inline_macro :ext do
    process do |parent, name, args|
      if args.any?
        parent.document.logger.fatal "macro ext:#{name}[] does not accept arguments"
      end

      RVFormat.process(self, parent, RVFormat.extension(name))
    end
  end

  inline_macro :csr do
    process do |parent, name, args|
      if args.size > 1
        parent.document.logger.fatal "macro csr:#{name}[] takes at most one argument"
      elsif name == ":" && args.empty?
        parent.document.logger.fatal "macro csr::[] takes exactly one argument"
      end

      name = name == ":" ? "" : name
      field = args.fetch(1, "")

      RVFormat.process(self, parent, RVFormat.csr(name, field))
    end
  end

  inline_macro :insnlink do
    process do |parent, name, args|
      RVFormat.process_xref(self, parent, RVFormat.instruction(name, args), "insn:#{name.downcase}")
    end
  end

  inline_macro :extlink do
    process do |parent, name, args|
      if args.any?
        parent.document.logger.fatal "macro extlink:#{name}[] does not accept arguments"
      end

      RVFormat.process_xref(self, parent, RVFormat.extension(name), "ext:#{name.downcase}")
    end
  end

  inline_macro :csrlink do
    process do |parent, name, args|
      if args.size > 1
        parent.document.logger.fatal "macro csrlink:#{name}[] takes at most one argument"
      end

      field = args.fetch(1, "")
      ref = "csr:#{name}#{field.empty? ? "" : "_#{field}"}".downcase

      RVFormat.process_xref(self, parent, RVFormat.csr(name, field), ref)
    end
  end
end

Asciidoctor::Extensions.register do
  postprocessor do
    process do |doc, output|
      # For each undefined reference, emit the same error asciidoctor would.
      Array(doc.attributes['RVFormat.xrefs']).each do |target|
        unless doc.catalog[:refs].key? target
          doc.logger.info "possible invalid reference: #{target}"
        end
      end

      output
    end
  end
end
