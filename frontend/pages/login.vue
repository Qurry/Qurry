<template>
  <v-row>
    <v-col>
      <h1>Login</h1>
      <MessageList :messages="errors" />
      <v-form v-model="isFormValid" @submit.prevent="onSubmit">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="email"
                :rules="[rules.required, rules.email]"
                label="Email"
                required
                class="form-field"
                color="secondary"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="password"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required]"
                label="Password"
                class="form-field"
                color="secondary"
                @click:append="showPassword = !showPassword"
              ></v-text-field>
            </v-col>
            <v-btn :disabled="!isFormValid" color="secondary" type="submit">
              Login
            </v-btn>
          </v-row>
        </v-container>
      </v-form>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ middleware: 'guest', auth: false })
export default class Register extends Vue {
  errors: string[] = []
  isFormValid = false
  email = ''
  password = ''
  showPassword = false
  rules = {
    required: (value: string) => !!value || 'Required.',
    email: (value: string) => {
      const pattern = /^[\w.-]*@([\w.-]+\.)?(hpi\.de|hpi\.uni-potsdam\.de)$/
      return pattern.test(value) || 'Please use an HPI Email.'
    },
  }

  onSubmit() {
    this.login()
  }

  login() {
    this.errors = []
    this.$auth
      .loginWith('local', {
        data: { email: this.email, password: this.password },
      })
      .then((_res: any) => {
        this.$nuxt.$emit('reload')
        this.$router.push('/questions')
      })
      .catch((error) => {
        this.errors.push(error.response.data.detail)
      })
  }
}
</script>

<style scoped>
.form-field {
  max-width: 300px;
}
</style>
