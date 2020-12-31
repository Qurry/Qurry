<template>
  <span ref="mathJaxEl" class="e-mathjax">{{ content }}</span>
</template>

<script>
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class MathJaxParser extends Vue {
  @Prop()
  content

  mounted() {
    this.renderMathJax()
  }

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
  }
}
</script>
