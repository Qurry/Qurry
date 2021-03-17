<template>
  <v-row>
    <v-col>
      <h1>Login</h1>
      <MessageList :messages="errors" />
      <v-form v-model="isFormValid" @submit.prevent="onSubmit">
        <v-container>
          <v-row>
            <v-col cols="12">
              <EmailInput v-model="user.email" class="form-field" />
            </v-col>
            <v-col cols="12">
              <PasswordInput v-model="user.password" class="form-field" />
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

interface LoginUser {
  email: string
  password: string
}

@Component({ middleware: 'guest', auth: false })
export default class Register extends Vue {
  errors: string[] = []
  isFormValid = false

  user: LoginUser = {
    email: '',
    password: '',
  }

  onSubmit() {
    this.login()
  }

  login() {
    this.errors = []
    this.$auth
      .loginWith('local', {
        data: this.user,
      })
      .then((_res: any) => {
        this.$nuxt.$emit('reload')
        this.$router.push('/questions')
      })
      .catch((error) => {
        if (error.response.data.errors) {
          this.errors.push(
            ...Object.values(error.response.data.errors as string)
          )
        } else {
          console.log(error)
        }
      })
  }
}
</script>

<style scoped>
.form-field {
  max-width: 300px;
}
</style>
