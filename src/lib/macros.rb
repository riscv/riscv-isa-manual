require 'asciidoctor'
require 'asciidoctor/extensions'

# Macro                 Expands to
#
# insn:foo[]            FOO
# insn:foo[bar,baz]     FOO bar, baz
#
# ext:zoo[]             `Zoo`
#
# extlink:zoo[]         <<ext:zoo, `Zoo`>>
#
# csr:foo[]             `foo`
# csr::[bar]            `BAR`
# csr:foo[bar]          `foo.BAR`
#
# csrlink:foo[]         <<csr:foo, `foo`>>
# csrlink:foo[bar]      <<csr:foo_bar, `foo.BAR`>>

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
end

Asciidoctor::Extensions.register do
  inline_macro :insn do
    process do |parent, name, args|
      create_inline parent, :quoted, parent.apply_subs(RVFormat.instruction(name, args), [:quotes])
    end
  end

  inline_macro :ext do
    process do |parent, name, args|
      if args.any?
        parent.document.logger.fatal "macro ext:#{name}[] does not accept arguments"
      end

      create_inline parent, :quoted, parent.apply_subs(RVFormat.extension(name), [:quotes])
    end
  end

  inline_macro :csr do
    process do |parent, name, args|
      str = name == ":" ? "" : "#{name.downcase}"

      if args.size > 1
        parent.document.logger.fatal "macro csr:#{name}[] takes at most one argument"
      elsif name == ":" && args.empty?
        parent.document.logger.fatal "macro csr::[] takes exactly one argument"
      end

      name = name == ":" ? "" : name
      field = args.fetch(1, "")

      create_inline parent, :quoted, parent.apply_subs(RVFormat.csr(name, field), [:quotes])
    end
  end
end
