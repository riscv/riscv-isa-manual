require 'asciidoctor/extensions' unless RUBY_ENGINE == 'opal'

include Asciidoctor

Extensions.register do
  # A treeprocessor that increments each level-1 section number by the value of
  # the `sectnumoffset` attribute. The numbers of all subsections will be
  # incremented automatically since those values are calculated dynamically.
  #
  # Run using:
  #
  #  asciidoctor -r ./lib/sectnumoffset-treeprocessor.rb -a sectnums -a sectnumoffset=1 lib/sectnumoffset-treeprocessor/sample.adoc
  #
  treeprocessor do
    process do |document|
      if (document.attr? 'sectnums') && (sectnumoffset = (document.attr 'sectnumoffset', 0).to_i) != 0
        if sectnumoffset > 0
          document.find_by(context: :section) {|sect| sect.level == 1 && sect.numbered }.each do |sect|
            sectnumoffset.times { sect.numeral = sect.numeral.next } rescue (sect.number += sectnumoffset)
          end
        else
          document.find_by(context: :section) {|sect| sect.level == 1 && sect.numbered }.each do |sect|
            sectnumoffset.abs.times { sect.numeral = sect.numeral.to_i.pred.to_s } rescue (sect.number += sectnumoffset)
          end
        end
      end
      nil
    end
  end
end
