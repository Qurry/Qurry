<template>
  <v-row>
    <v-col>
      <h1>Forgot Password</h1>
      <p>Please enter your email address to request a reset link.</p>
      <MessageList :messages="errors" />
      <v-form v-model="isFormValid" @submit.prevent="onSubmit">
        <v-container>
          <v-row>
            <v-col cols="12">
              <EmailInput v-model="email" class="form-field" />
            </v-col>
            <v-btn
              :disabled="!isFormValid || loading"
              :loading="loading"
              color="secondary"
              type="submit"
            >
              Submit
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
export default class ForgottenPassword extends Vue {
  email = ''

  errors: string[] = []
  isFormValid = false
  loading = false

  onSubmit() {
    this.loading = true
    this.errors = []
    this.requestPasswordReset()
      .then((_res: any) => {
        this.$router.push('/password/confirm')
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

  async requestPasswordReset() {
    const response = await this.$axios.post('/forgotpassword/', {
      email: this.email,
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
