<template>
  <v-row>
    <v-col>
      <h1>Registierung</h1>
      <p>
        Zur Zeit ist die Registierung nur für HPI Studenten mit einer HPI E-mail
        Adresse möglich.
      </p>
      <v-form v-model="isFormValid">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="username"
                :rules="[
                  rules.required,
                  rules.minLengthUsername,
                  rules.maxLength,
                  rules.charsUsername,
                ]"
                label="Nutzername"
                required
                class="form-field"
                color="secondary"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="email"
                :rules="[rules.required, rules.email]"
                label="E-mail"
                required
                class="form-field"
                color="secondary"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="password"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[
                  rules.required,
                  rules.minLengthPassword,
                  rules.maxLength,
                  rules.number,
                  rules.uppercase,
                  rules.lowercase,
                ]"
                :type="showPassword ? 'text' : 'password'"
                label="Passwort"
                class="form-field"
                color="secondary"
                @click:append="showPassword = !showPassword"
              ></v-text-field>
            </v-col>
            <v-btn :disabled="!isFormValid" color="secondary" @click="onSubmit">
              Registrieren
            </v-btn>
          </v-row>
        </v-container>
      </v-form>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import UserService from './../../services/UserService'

@Component({ middleware: 'guest', auth: false })
export default class Register extends Vue {
  isFormValid = false
  username = ''
  email = ''
  password = ''
  showPassword = false
  rules = {
    required: (value: string) => !!value || 'Erforderlich.',
    minLengthPassword: (value: string) =>
      value.length >= 10 || 'Mindestens 10 Zeichen',
    minLengthUsername: (value: string) =>
      value.length >= 3 || 'Mindestens 3 Zeichen',
    charsUsername: (value: string) =>
      /^[a-zA-Z][a-zA-Z0-9._-]*$/.test(value) || 'Unerlaubte Zeichen',
    number: (value: string) => /\d/.test(value) || 'Mindestens eine Zahl',
    lowercase: (value: string) =>
      /[a-z]/.test(value) || 'Mindestens ein Kleinbuchstabe',
    uppercase: (value: string) =>
      /[A-Z]/.test(value) || 'Mindestens ein Großbuchstabe',
    maxLength: (value: string) => value.length <= 100 || 'Maximal 100 Zeichen',
    email: (value: string) => {
      const pattern = /^[a-zA-Z.-]*@[a-zA-Z.-]*(hpi.de|hpi.uni-potsdam.de)$/
      return pattern.test(value) || 'Ungültige E-Mail'
    },
  }

  onSubmit() {
    UserService.register(this.username, this.email, this.password)
      .then((res: any) => {
        console.log(res)
      })
      .catch((error) => console.log(error))
  }
}
</script>

<style scoped>
.form-field {
  max-width: 300px;
}
</style>
