/*!
 * reveal.js plugin that adds extra functionality for Sphinx.
 * Code highlighting support taken from the original highlight plugin by hakimel
 */

const Plugin = {

  id: 'sphinx_revealit',

  HIGHLIGHT_STEP_DELIMITER: '|',
  HIGHLIGHT_LINE_DELIMITER: ',',
  HIGHLIGHT_LINE_RANGE_DELIMITER: '-',

  /**
   * Highlights code blocks withing the given deck.
   *
   * Note that this can be called multiple times if
   * there are multiple presentations on one page.
   *
   * @param {Reveal} reveal the reveal.js instance
   */
  init: function(reveal) {

    // Read the plugin config options and provide fallbacks
    /*
    var config = reveal.getConfig().highlight || {};
    config.highlightOnLoad = typeof config.highlightOnLoad === 'boolean' ? config.highlightOnLoad : true;
    config.escapeHTML = typeof config.escapeHTML === 'boolean' ? config.escapeHTML : true;
    */

    [].slice.call(reveal.getRevealElement().querySelectorAll('.highlight code')).forEach(function(block) {

      if(block.hasAttribute('data-line-numbers')) {
        var scrollState = {currentBlock: block};

        // If there is at least one highlight step, generate
        // fragments
        var highlightSteps = Plugin.deserializeHighlightSteps(block.getAttribute('data-line-numbers'));
        if(highlightSteps.length > 1) {

          // If the original code block has a fragment-index,
          // each clone should follow in an incremental sequence
          var fragmentIndex = parseInt(block.getAttribute('data-fragment-index'), 10);

          if(typeof fragmentIndex !== 'number' || isNaN(fragmentIndex)) {
            fragmentIndex = null;
          }

          // Generate fragments for all steps except the original block
          highlightSteps.slice(1).forEach(function(highlight) {

            var fragmentBlock = block.cloneNode(true);
            fragmentBlock.setAttribute('data-line-numbers', Plugin.serializeHighlightSteps([highlight]));
            fragmentBlock.classList.add('fragment');
            block.parentNode.appendChild(fragmentBlock);
            Plugin.highlightLines(fragmentBlock);

            if(typeof fragmentIndex === 'number') {
              fragmentBlock.setAttribute('data-fragment-index', fragmentIndex);
              fragmentIndex += 1;
            }
            else {
              fragmentBlock.removeAttribute('data-fragment-index');
            }

            // Scroll highlights into view as we step through them
            fragmentBlock.addEventListener('visible', Plugin.scrollHighlightedLineIntoView.bind(Plugin, fragmentBlock, scrollState));
            fragmentBlock.addEventListener('hidden', Plugin.scrollHighlightedLineIntoView.bind(Plugin, fragmentBlock.previousSibling, scrollState));

          });

          block.removeAttribute('data-fragment-index')
          block.setAttribute('data-line-numbers', Plugin.serializeHighlightSteps([highlightSteps[0]]));

        }

        // Scroll the first highlight into view when the slide
        // becomes visible. Note supported in IE11 since it lacks
        // support for Element.closest.
        var slide = typeof block.closest === 'function' ? block.closest('section:not(.stack)') : null;
        if(slide) {
          var scrollFirstHighlightIntoView = function() {
            Plugin.scrollHighlightedLineIntoView(block, scrollState, true);
            slide.removeEventListener('visible', scrollFirstHighlightIntoView);
          }
          slide.addEventListener('visible', scrollFirstHighlightIntoView);
        }

        Plugin.highlightLines(block);

      }

    });

    // If we're printing to PDF, scroll the code highlights of
    // all blocks in the deck into view at once
    reveal.on('pdf-ready', function() {
      [].slice.call(reveal.getRevealElement().querySelectorAll('pre code[hl-lines].current-fragment')).forEach(function(block) {
        Plugin.scrollHighlightedLineIntoView(block, {}, true);
      });
    });

  },

  /**
   * Animates scrolling to the first highlighted line
   * in the given code block.
   */
  scrollHighlightedLineIntoView: function(block, scrollState, skipAnimation) {

    cancelAnimationFrame(scrollState.animationFrameID);

    // Match the scroll position of the currently visible
    // code block
    if(scrollState.currentBlock) {
      block.scrollTop = scrollState.currentBlock.scrollTop;
    }

    // Remember the current code block so that we can match
    // its scroll position when showing/hiding fragments
    scrollState.currentBlock = block;

    var highlightBounds = this.getHighlightedLineBounds(block)
    var viewportHeight = block.offsetHeight;

    // Subtract padding from the viewport height
    var blockStyles = getComputedStyle(block);
    viewportHeight -= parseInt(blockStyles.paddingTop) + parseInt(blockStyles.paddingBottom);

    // Scroll position which centers all highlights
    var startTop = block.scrollTop;
    var targetTop = highlightBounds.top + (Math.min(highlightBounds.bottom - highlightBounds.top, viewportHeight) - viewportHeight) / 2;

    // Account for offsets in position applied to the
    // <table> that holds our lines of code
    var lineTable = block.querySelector('.hljs-ln');
    if(lineTable) targetTop += lineTable.offsetTop - parseInt(blockStyles.paddingTop);

    // Make sure the scroll target is within bounds
    targetTop = Math.max(Math.min(targetTop, block.scrollHeight - viewportHeight), 0);

    if(skipAnimation === true || startTop === targetTop) {
      block.scrollTop = targetTop;
    }
    else {

      // Don't attempt to scroll if there is no overflow
      if(block.scrollHeight <= viewportHeight) return;

      var time = 0;
      var animate = function() {
        time = Math.min(time + 0.02, 1);

        // Update our eased scroll position
        block.scrollTop = startTop + (targetTop - startTop) * Plugin.easeInOutQuart(time);

        // Keep animating unless we've reached the end
        if(time < 1) {
          scrollState.animationFrameID = requestAnimationFrame(animate);
        }
      };

      animate();

    }

  },

  /**
   * The easing function used when scrolling.
   */
  easeInOutQuart: function(t) {

    // easeInOutQuart
    return t < .5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t;

  },

  getHighlightedLineBounds: function(block) {

    var highlightedLines = block.querySelectorAll('.highlight-line');
    if(highlightedLines.length === 0) {
      return {top: 0, bottom: 0};
    }
    else {
      var firstHighlight = highlightedLines[0];
      var lastHighlight = highlightedLines[highlightedLines.length - 1];

      return {
        top: firstHighlight.offsetTop,
        bottom: lastHighlight.offsetTop + lastHighlight.offsetHeight
      }
    }

  },

  /**
   * Visually emphasize specific lines within a code block.
   * This only works on blocks with line numbering turned on.
   *
   * @param {HTMLElement} block a <code> block
   * @param {String} [linesToHighlight] The lines that should be
   * highlighted in this format:
   * "1"    = highlights line 1
   * "2,5"  = highlights lines 2 & 5
   * "2,5-7"  = highlights lines 2, 5, 6 & 7
   */
  highlightLines: function(block, linesToHighlight) {

    var highlightSteps = Plugin.deserializeHighlightSteps(linesToHighlight || block.getAttribute('data-line-numbers'));

    if(highlightSteps.length) {

      highlightSteps[0].forEach(function(highlight) {

        var elementsToHighlight = [];

        // Highlight a range
        if(typeof highlight.end === 'number') {
          elementsToHighlight = [].slice.call(block.querySelectorAll('table tr:nth-child(n+' + highlight.start + '):nth-child(-n+' + highlight.end + ')'));
        }
        // Highlight a single line
        else
          if(typeof highlight.start === 'number') {
            elementsToHighlight = [].slice.call(block.querySelectorAll('table tr:nth-child(' + highlight.start + ')'));
          }

        if(elementsToHighlight.length) {
          elementsToHighlight.forEach(function(lineElement) {
            lineElement.classList.add('highlight-line');
          });

          block.classList.add('has-highlights');
        }

      });

    }

  },

  /**
   * Parses and formats a user-defined string of line
   * numbers to highlight.
   *
   * @example
   * Plugin.deserializeHighlightSteps( '1,2|3,5-10' )
   * // [
   * //   [ { start: 1 }, { start: 2 } ],
   * //   [ { start: 3 }, { start: 5, end: 10 } ]
   * // ]
   */
  deserializeHighlightSteps: function(highlightSteps) {
    if(!highlightSteps) return {};

    // Remove whitespace
    highlightSteps = highlightSteps.replace(/\s/g, '');

    // Divide up our line number groups
    highlightSteps = highlightSteps.split(Plugin.HIGHLIGHT_STEP_DELIMITER);

    return highlightSteps.map(function(highlights) {

      return highlights.split(Plugin.HIGHLIGHT_LINE_DELIMITER).map(function(highlight) {

        // Parse valid line numbers
        if(/^[\d-]+$/.test(highlight)) {

          highlight = highlight.split(Plugin.HIGHLIGHT_LINE_RANGE_DELIMITER);

          var lineStart = parseInt(highlight[0], 10),
            lineEnd = parseInt(highlight[1], 10);

          if(isNaN(lineEnd)) {
            return {
              start: lineStart
            };
          }
          else {
            return {
              start: lineStart,
              end: lineEnd
            };
          }

        }
        // If no line numbers are provided, no code will be highlighted
        else {

          return {};

        }

      });

    });

  },

  /**
   * Serializes parsed line number data into a string so
   * that we can store it in the DOM.
   */
  serializeHighlightSteps: function(highlightSteps) {

    return highlightSteps.map(function(highlights) {

      return highlights.map(function(highlight) {

        // Line range
        if(typeof highlight.end === 'number') {
          return highlight.start + Plugin.HIGHLIGHT_LINE_RANGE_DELIMITER + highlight.end;
        }
        // Single line
        else
          if(typeof highlight.start === 'number') {
            return highlight.start;
          }
          // All lines
          else {
            return '';
          }

      }).join(Plugin.HIGHLIGHT_LINE_DELIMITER);

    }).join(Plugin.HIGHLIGHT_STEP_DELIMITER);

  }
};

this.sphinx_revealit = Plugin
