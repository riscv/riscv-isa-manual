'use strict'

/**
 * Asciidoctor.js port of src/lib/macros.rb for use with asciidoctor-web-pdf.
 *
 * Inline macros provided:
 *
 *   insn:foo[]              FOO
 *   insn:foo[rd,rs1,rs2]    FOO rd, rs1, rs2   (args joined with non-breaking space)
 *
 *   insnlink:foo[]          <a href="#insn:foo">FOO</a>
 *
 *   ext:v[]                 <code>V</code>
 *
 *   extlink:v[]             <a href="#ext:v"><code>V</code></a>
 *
 *   csr:foo[]               <code>foo</code>
 *   csr::[FIELD]            <code>FIELD</code>      (field-only form; empty target)
 *   csr:foo[FIELD]          <code>foo.⁠FIELD</code> (word-joiner prevents break at dot)
 *
 *   csrlink:foo[]           <a href="#csr:foo"><code>foo</code></a>
 *   csrlink:foo[FIELD]      <a href="#csr:foo_field"><code>foo.⁠FIELD</code></a>
 *
 *   qty:16[KiB]             16&nbsp;KiB
 *
 * Loaded via:  --require ./src/lib/macros-extensions.js
 */

const NBSP = ' '  // non-breaking space
const WJ   = '⁠'  // word joiner — prevents line-break at the dot in csr:foo[FIELD]

// ---------------------------------------------------------------------------
// Formatting helpers  (mirror RVFormat module in macros.rb)
// ---------------------------------------------------------------------------

function instruction (target, attrs) {
  const args = positionalAttrs(attrs)
  return target.toUpperCase() + (args.length ? NBSP : '') + args.join(',' + NBSP)
}

function extension (target) {
  // Capitalise first character, leave the rest as-is.
  return target.charAt(0).toUpperCase() + target.slice(1)
}

function csrText (name, field) {
  const parts = []
  if (name)  parts.push(name.toLowerCase())
  if (field) parts.push(field.toUpperCase())
  return parts.join('.' + WJ)
}

// Collect positional attributes from the attrs object.
// Asciidoctor.js passes the entire bracket content as attrs['text'], e.g.
//   insn:add[rd,rs1,rs2]  →  attrs['text'] = 'rd,rs1,rs2'
// Split on commas and trim whitespace to recover the individual positional args.
function positionalAttrs (attrs) {
  const text = attrs['text'] || ''
  if (!text) return []
  return text.split(',').map(s => s.trim())
}

function esc (str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

// ---------------------------------------------------------------------------
// Node factories
// ---------------------------------------------------------------------------

// Plain or monospaced inline text — no link.
function inlineText (proc, parent, text, mono) {
  if (mono) {
    // createInline with type:'monospaced' emits <code>text</code> via the
    // HTML5 converter's convert_inline_quoted handler.
    return proc.createInline(parent, 'quoted', text, { type: 'monospaced' })
  }
  // type:'unquoted' returns node.text verbatim in the HTML5 converter —
  // no wrapper element and no additional escaping.
  return proc.createInline(parent, 'quoted', text, { type: 'unquoted' })
}

// Linked text: <a href="#ref">[<code>]label[</code>]</a>.
// We build the HTML directly and pass it through as an unquoted inline node.
// The HTML5 converter for :unquoted returns node.text verbatim so angle
// brackets are not re-escaped.
function inlineLink (proc, parent, label, ref, mono) {
  const inner = mono ? `<code>${esc(label)}</code>` : esc(label)
  const html  = `<a href="#${esc(ref)}">${inner}</a>`
  return proc.createInline(parent, 'quoted', html, { type: 'unquoted' })
}

// ---------------------------------------------------------------------------
// Extension registration
// ---------------------------------------------------------------------------

function register (Extensions) {
  Extensions.register(function () {

    // ── insn:foo[] / insn:foo[rd,rs1,rs2] ───────────────────────────────────
    this.inlineMacro(function () {
      this.named('insn')
      this.process(function (parent, target, attrs) {
        return inlineText(this, parent, instruction(target, attrs), false)
      })
    })

    // ── insnlink:foo[] ───────────────────────────────────────────────────────
    this.inlineMacro(function () {
      this.named('insnlink')
      this.process(function (parent, target, attrs) {
        const label = instruction(target, attrs)
        const ref   = 'insn:' + target.toLowerCase()
        return inlineLink(this, parent, label, ref, false)
      })
    })

    // ── ext:v[] ──────────────────────────────────────────────────────────────
    this.inlineMacro(function () {
      this.named('ext')
      this.process(function (parent, target, attrs) {
        return inlineText(this, parent, extension(target), true)
      })
    })

    // ── extlink:v[] ──────────────────────────────────────────────────────────
    this.inlineMacro(function () {
      this.named('extlink')
      this.process(function (parent, target, attrs) {
        const label = extension(target)
        const ref   = 'ext:' + target.toLowerCase()
        return inlineLink(this, parent, label, ref, true)
      })
    })

    // ── csr:foo[] / csr::[FIELD] / csr:foo[FIELD] ───────────────────────────
    // When the source is csr::[FIELD] Asciidoctor passes target as ':' (the
    // extra colon becomes the target string).  We treat ':' as an empty name.
    this.inlineMacro(function () {
      this.named('csr')
      this.process(function (parent, target, attrs) {
        const name  = (target === ':') ? '' : target
        const field = attrs['text'] || ''
        return inlineText(this, parent, csrText(name, field), true)
      })
    })

    // ── csrlink:foo[] / csrlink:foo[FIELD] ──────────────────────────────────
    this.inlineMacro(function () {
      this.named('csrlink')
      this.process(function (parent, target, attrs) {
        const field = attrs['text'] || ''
        const label = csrText(target, field)
        const ref   = ('csr:' + target + (field ? '_' + field : '')).toLowerCase()
        return inlineLink(this, parent, label, ref, true)
      })
    })

    // ── qty:16[KiB] ──────────────────────────────────────────────────────────
    this.inlineMacro(function () {
      this.named('qty')
      this.process(function (parent, target, attrs) {
        const unit = attrs['text'] || ''
        return inlineText(this, parent, target + NBSP + unit, false)
      })
    })

  })
}

module.exports = { register }
