<template>
  <v-row>
    <v-col>
      <h1>Set New Password</h1>
      <MessageList :messages="errors" />
      <v-form v-model="isFormValid" @submit.prevent="onSubmit">
        <v-container>
          <v-row>
            <v-col cols="12">
              <PasswordInput
                v-model="password"
                class="form-field"
                creation-mode="true"
              />
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
export default class ResetPassword extends Vue {
  password = ''

  errors: string[] = []
  isFormValid = false
  loading = false

  onSubmit() {
    this.loading = true
    this.errors = []
    this.resetPassword()
      .then((_res: any) => {
        this.$router.push('/login')
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

  async resetPassword() {
    const response = await this.$axios.post('/resetpassword/', {
      password: this.password,
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
