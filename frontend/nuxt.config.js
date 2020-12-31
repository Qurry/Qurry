import colors from 'vuetify/es5/util/colors'

export default {
  // Disable server-side rendering (https://go.nuxtjs.dev/ssr-mode)
  ssr: false,

  // Target (https://go.nuxtjs.dev/config-target)
  target: 'static',

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: 'Qurry',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content:
          'Qurry is the place where students can ask their questions in an uncomplicated and informal way. The questions can be organisational or content-related. Together, the best approaches to solving assignments can be discussed.',
      },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [{ src: '~/plugins/prism', mode: 'client' }, '~plugins/filters.ts'],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  modules: ['@nuxtjs/axios', '@nuxtjs/auth'],

  auth: {
    strategies: {
      local: {
        endpoints: {
          login: {
            url: '/token/generate',
            method: 'post',
            propertyName: 'access',
          },
          logout: false,
          user: false,
        },
      },
    },
  },

  router: {
    middleware: ['auth'],
  },

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    credentials: true,
    init(axios) {
      axios.defaults.withCredentials = true
    },
    baseURL: 'http://localhost:8000/api',
  },

  // Vuetify module configuration (https://go.nuxtjs.dev/config-vuetify)
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      light: true,
      themes: {
        light: {
          primary: '#e55c44', // orange
          accent: '#f6ae2d', // yellow
          secondary: '#33658a', // blue
          darkblue: '#2f4858',
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },

  env: {
    API_URL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    // * You can extend webpack config here
    vendor: ['axios', 'prismjs'],

    extend(config, ctx) {
      if (ctx.isServer) {
        config.externals = [
          nodeExternals({
            whitelist: [/^vuetify/],
          }),
        ]
      }
    },
  },
}
