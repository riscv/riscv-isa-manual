require 'asciidoctor'
require 'asciidoctor/extensions'

Asciidoctor::Extensions.register do
  inline_macro :insn do
    # convert insn:foo[] to FOO
    # convert insn:foo[bar,baz] to FOO bar, baz
    process do |parent, name, args|
      str = name.upcase

      if args.any?
        str = "#{str}\u{a0}#{args.values.join(",\u{a0}")}"
      end

      create_inline parent, :quoted, str
    end
  end

  inline_macro :ext do
    # convert ext:foo[] to `Foo`
    process do |parent, name, args|
      unless args.empty?
        parent.document.logger.fatal "macro ext:#{name}[] does not accept arguments"
      end

      str = "`#{name.capitalize}`"
      str = parent.apply_subs(str, [:quotes])

      create_inline parent, :quoted, str
    end
  end

  inline_macro :csr do
    # convert csr:foo[] to `foo`
    # convert csr::[bar] to `BAR`
    # convert csr:foo[bar] to `foo.BAR`
    process do |parent, name, args|
      str = name == ":" ? "" : "#{name.downcase}"

      if args.size == 1
        str += ".\u{2060}" unless str.empty?
        str += args[1].upcase
      elsif args.size > 1
        parent.document.logger.fatal "macro csr:#{name}[] takes at most one argument"
      end

      str = "`#{str}`"
      str = parent.apply_subs(str, [:quotes])

      create_inline parent, :quoted, str
    end
  end
end
