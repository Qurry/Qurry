<template>
  <div>
    <span ref="mathJaxEl" class="e-mathjax">{{ data }}</span>
  </div>
</template>

//
<script>
export default {
  props: ['data'],

  mounted() {
    this.renderMathJax()
  },

  methods: {
    // readMD() {
    //   return this.$md.render(this.data)
    // },

    renderMathJax() {
      if (window.MathJax) {
        window.MathJax.Hub.Config({
          tex2jax: {
            inlineMath: [['$', '$']],
            displayMath: [['$$', '$$']],
            processEscapes: true,
            processEnvironments: true,
          },
          // Center justify equations in code and markdown cells. Elsewhere
          // we use CSS to left justify single line equations in code cells.
          displayAlign: 'center',
          'HTML-CSS': {
            styles: { '.MathJax_Display': { margin: 0 } },
            linebreaks: { automatic: true },
          },
        })
        window.MathJax.Hub.Queue([
          'Typeset',
          window.MathJax.Hub,
          this.$refs.mathJaxEl,
        ])
      }
    },
  },
}
</script>
