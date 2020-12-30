<template>
  <v-row>
    <v-col>
      <h1>Anmelden</h1>
      <ul>
        <li v-for="(error, i) of errors" :key="i">
          {{ error }}
        </li>
      </ul>
      <v-form v-model="isFormValid">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="email"
                :rules="[rules.required]"
                label="E-Mail"
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
                label="Passwort"
                class="form-field"
                color="secondary"
                @click:append="showPassword = !showPassword"
              ></v-text-field>
            </v-col>
            <v-btn :disabled="!isFormValid" color="secondary" @click="login">
              Anmelden
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
    required: (value: string) => !!value || 'Erforderlich.',
    email: (value: string) => {
      const pattern = /^[a-zA-Z.-]*@[a-zA-Z.-]*(hpi.de|hpi.uni-potsdam.de)$/
      return pattern.test(value) || 'Ungültige E-Mail'
    },
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
        console.log(error.response.data.detail)
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
