import Vue from 'vue'
import VMdPreview from '@kangc/v-md-editor/lib/preview'
import VueMarkdownEditor from '@kangc/v-md-editor'
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js'
import createKatexPlugin from '@kangc/v-md-editor/lib/plugins/katex/cdn'
import enUS from '@kangc/v-md-editor/lib/lang/en-US'

import '@kangc/v-md-editor/lib/style/preview.css'
import '@kangc/v-md-editor/lib/style/base-editor.css'
import '@kangc/v-md-editor/lib/theme/style/github.css'

VMdPreview.use(githubTheme)
VMdPreview.use(createKatexPlugin())

VueMarkdownEditor.use(githubTheme)
VueMarkdownEditor.use(createKatexPlugin())
VueMarkdownEditor.lang.use('en-US', enUS)

Vue.use(VMdPreview)
Vue.use(VueMarkdownEditor)
