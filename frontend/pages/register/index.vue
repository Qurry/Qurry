<template>
  <v-row>
    <v-col>
      <h1>Registration</h1>
      <p>
        At the moment registration is only possible for
        <a href="https://hpi.de/" target="_blank">HPI</a> students with an HPI
        email address.
      </p>
      <MessageList :messages="errors" />
      <v-form v-model="isFormValid">
        <v-container>
          <v-row>
            <v-col cols="12">
              <UsernameInput
                v-model="user.username"
                class="form-field"
                creation-mode="true"
              />
            </v-col>
            <v-col cols="12">
              <EmailInput v-model="user.email" class="form-field" />
            </v-col>
            <v-col cols="12">
              <PasswordInput
                v-model="user.password"
                class="form-field"
                creation-mode="true"
              />
            </v-col>
            <v-btn
              :disabled="!isFormValid || loading"
              :loading="loading"
              color="secondary"
              @click="onSubmit"
            >
              Register
            </v-btn>
          </v-row>
        </v-container>
      </v-form>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

export interface RegistrationUser {
  username: string
  email: string
  password: string
}

@Component({ middleware: 'guest', auth: false })
export default class Register extends Vue {
  user: RegistrationUser = {
    username: '',
    email: '',
    password: '',
  }

  errors: string[] = []
  isFormValid = false
  loading = false

  onSubmit() {
    this.loading = true
    this.errors = []
    this.register()
      .then((_res: any) => {
        this.$router.push('/register/confirm')
      })
      .catch((error) => {
        if (error.response.data.errors) {
          this.errors.push(
            ...Object.values(error.response.data.errors as string)
          )
        } else {
          console.log(error)
        }
        this.loading = false
      })
  }

  async register() {
    const bodyFormData = new FormData()
    bodyFormData.append('username', this.user.username)
    bodyFormData.append('email', this.user.email)
    bodyFormData.append('password', this.user.password)

    const response = await this.$axios.post('/register/', bodyFormData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response
  }
}
</script>

<style scoped>
.form-field {
  max-width: 300px;
}
</style>
