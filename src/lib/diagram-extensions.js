'use strict'

/**
 * Asciidoctor.js extensions for asciidoctor-web-pdf:
 *
 *  1. wavedrom block processor  — renders register/waveform diagrams to SVG
 *  2. bytefield block processor — renders byte-field diagrams to SVG
 *  3. cover page postprocessor  — rebuilds the minimal asciidoctor-web-pdf
 *     title page to match the original asciidoctor-pdf cover (RISC-V logo,
 *     title, revision number, release description).
 *
 * Loaded via:  --require ./src/lib/diagram-extensions.js
 */

const fs   = require('fs')
const path = require('path')
const root = path.resolve(__dirname, '../../')

// ---------------------------------------------------------------------------
// wavedrom — uses the wavedrom npm package (pure-JS SVG renderer)
// WaveDrom source uses JS object notation (unquoted keys), so we use json5.
// ---------------------------------------------------------------------------
const wavedrom = require(path.join(root, 'node_modules/wavedrom/lib/index.js'))
const skin     = require(path.join(root, 'node_modules/wavedrom/skins/default.js'))
const JSON5    = require(path.join(root, 'node_modules/json5/lib/index.js'))

function renderWavedrom (source) {
  let parsed
  try {
    parsed = JSON5.parse(source.trim())
  } catch (e) {
    console.warn('[diagram-extensions] wavedrom: parse error:', e.message)
    return `<pre class="diagram-error">wavedrom parse error: ${e.message}\n${source}</pre>`
  }
  try {
    const tree = wavedrom.renderAny(0, parsed, skin)
    return wavedrom.onml.stringify(tree)
  } catch (e) {
    console.warn('[diagram-extensions] wavedrom: render error:', e.message)
    return `<pre class="diagram-error">wavedrom render error: ${e.message}</pre>`
  }
}

// ---------------------------------------------------------------------------
// bytefield-svg — compiled ClojureScript; lib.La(source) returns SVG string
// ---------------------------------------------------------------------------
const bytefield = require(path.join(root, 'node_modules/bytefield-svg/lib.js'))

function renderBytefield (source) {
  try {
    return bytefield.La(source)
  } catch (e) {
    console.warn('[diagram-extensions] bytefield: render error:', e.message)
    return `<pre class="diagram-error">bytefield render error: ${e.message}</pre>`
  }
}

// ---------------------------------------------------------------------------
// Normalise SVG dimensions so diagrams scale to page/column width.
//
// Both wavedrom and bytefield-svg emit hard-coded pixel widths (e.g.
// width="800") on the root <svg> element.  In Chromium's renderer, explicit
// SVG attributes override CSS, so max-width rules have no effect.  We replace
// the fixed width with "100%" and remove the fixed height attribute entirely
// (letting viewBox drive the aspect ratio) so paged.js can fit the diagram
// to the text area.  Setting height="auto" is invalid SVG and Chromium rejects it.
// ---------------------------------------------------------------------------
function normaliseSvgDimensions (svg) {
  return svg
    .replace(/(<svg\b[^>]*)\bwidth="[^"]*"/,  '$1width="100%"')
    .replace(/(<svg\b[^>]*)\s+height="[^"]*"/, '$1')
}

// ---------------------------------------------------------------------------
// Convert SVG to a data-URI <img> so paged.js treats it as atomic replaced
// content rather than traversing its DOM subtree for page-break calculations.
// With 400+ diagrams in the full spec, inline SVGs create a massive DOM that
// causes paged.js to time out; opaque <img> elements are laid out trivially.
// ---------------------------------------------------------------------------
function svgToImgTag (svg) {
  const normSvg    = normaliseSvgDimensions(svg)
  // Extract viewBox to set an explicit aspect ratio via width/height attrs on
  // the <img> so browsers can reserve the correct space before the image loads.
  const vbMatch    = normSvg.match(/viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"/)
  const sizeAttrs  = vbMatch
    ? ` width="${vbMatch[1]}" height="${vbMatch[2]}"`
    : ''
  const dataUri    = 'data:image/svg+xml;base64,' +
    Buffer.from(normSvg).toString('base64')
  return `<img src="${dataUri}"${sizeAttrs} alt="diagram" style="max-width:100%;height:auto;">`
}

// ---------------------------------------------------------------------------
// Wrap diagram in a figure-like div so CSS can target it the same way as images
// ---------------------------------------------------------------------------
function wrapSvg (svg, attrs) {
  const title = attrs.title ? `<div class="diagram-title">${attrs.title}</div>` : ''
  return `<div class="imageblock diagram">\n<div class="content">${svgToImgTag(svg)}</div>\n${title}\n</div>`
}

// ---------------------------------------------------------------------------
// Cover page — build a data URI for the RISC-V logo so it can be embedded
// directly in the HTML without needing filesystem access from the browser.
// ---------------------------------------------------------------------------
function logoDataUri () {
  const logoPath = path.join(root, 'docs-resources/images/risc-v_logo.png')
  try {
    const data = fs.readFileSync(logoPath)
    return `data:image/png;base64,${data.toString('base64')}`
  } catch (e) {
    console.warn('[diagram-extensions] cover: could not read logo:', e.message)
    return null
  }
}

const LOGO_URI = logoDataUri()

// ---------------------------------------------------------------------------
// Extension registration — called by asciidoctor CLI with the Extensions registry
//
// @asciidoctor/core's Extensions object uses Extensions.register(fn) where fn
// is called with `this` bound to the registry scope that exposes this.block().
// ---------------------------------------------------------------------------
function register (Extensions) {
  Extensions.register(function () {
    // ── wavedrom ────────────────────────────────────────────────────────────
    this.block(function () {
      this.named('wavedrom')
      // wavedrom blocks use .... (literal) delimiters
      this.onContext(['listing', 'literal', 'open'])

      this.process(function (parent, reader, attrs) {
        const source = reader.getLines().join('\n')
        const svg    = renderWavedrom(source)
        const html   = wrapSvg(svg, attrs)
        return this.createBlock(parent, 'pass', html)
      })
    })

    // ── bytefield ───────────────────────────────────────────────────────────
    this.block(function () {
      this.named('bytefield')
      // bytefield blocks use ---- (listing) delimiters
      this.onContext(['listing', 'literal', 'open'])

      this.process(function (parent, reader, attrs) {
        const source = reader.getLines().join('\n')
        const svg    = renderBytefield(source)
        const html   = wrapSvg(svg, attrs)
        return this.createBlock(parent, 'pass', html)
      })
    })

    // ── cover page ──────────────────────────────────────────────────────────
    // asciidoctor-web-pdf generates a minimal cover:
    //   <div id="cover" class="title-page front-matter"><h1>…</h1></div>
    // It ignores :title-logo-image: and :back-cover-image: (asciidoctor-pdf
    // attributes).  This postprocessor replaces that div with a full cover
    // containing the RISC-V logo, title, revision number, and release remark.
    this.postprocessor(function () {
      this.process(function (document, output) {
        const title     = document.getDocumentTitle({ sanitize: true, use_fallback: true })
        const revnumber = document.getAttribute('revnumber', '')
        const revremark = document.getAttribute('revremark', '')

        const logoHtml   = LOGO_URI
          ? `<img class="cover-logo" src="${LOGO_URI}" alt="RISC-V International">`
          : ''
        const revHtml    = revnumber
          ? `<p class="cover-revnumber">${revnumber}</p>`
          : ''
        const remarkHtml = revremark
          ? `<p class="cover-remark">${revremark}</p>`
          : ''

        const newCover = [
          '<div id="cover" class="title-page front-matter">',
          '  <div class="cover-inner">',
          `    ${logoHtml}`,
          `    <h1 class="cover-title">${title}</h1>`,
          `    ${revHtml}`,
          `    ${remarkHtml}`,
          '  </div>',
          '</div>',
        ].join('\n')

        // The existing cover div contains only an <h1> (and optional <h2>),
        // so matching up to the first </div> after id="cover" is safe.
        return output.replace(
          /<div id="cover"[^>]*>[\s\S]*?<\/div>/,
          newCover
        )
      })
    })
  })
}

module.exports = { register }
