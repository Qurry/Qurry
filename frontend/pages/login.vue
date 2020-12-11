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
                @click:append="showPassword = !showPassword"
              ></v-text-field>
            </v-col>
            <v-btn :disabled="!isFormValid" color="orange" @click="login">
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

@Component({ middleware: 'guest' })
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

  // async (): Promise<Array<Employee> | string> =>

  // async login() {
  //   try {
  //     const response: any = await this.$auth.loginWith('local', {
  //       data: { email: this.email, password: this.password },
  //     })
  //     console.log("here")
  //     console.log(response)
  //     console.log(response.ok)
  //     if (!response.ok) throw new Error(response.statusText)
  //     const { data } = await response.json()
  //     console.log(data)
  //     // process body
  //   } catch (err) {
  //     console.log("hereerr")
  //     console.log(err)
  //     console.log(err.message)
  //     const { data } = await err.json()
  //     console.log(data)
  //   }
  //   // try {
  //   //   const res = await this.$auth.loginWith('local', {
  //   //     data: { email: this.email, password: this.password },
  //   //   })
  //   //   console.log(res.status)
  //   // } catch (err) {
  //   //   console.log(err)
  //   // }
  // }

  login() {
    this.errors = []
    this.$auth
      .loginWith('local', {
        data: { email: this.email, password: this.password },
      })
      .then((response: any) => {
        console.log(response)
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
