<template>
  <v-menu offset-y>
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        v-bind="attrs"
        v-on="on"
        @click="$store.dispatch('getNotifications')"
      >
        <v-badge
          v-if="$store.state.numOfUnreadNotifications"
          color="secondary"
          :content="$store.state.numOfUnreadNotifications"
        >
          <v-icon> mdi-email </v-icon>
        </v-badge>
        <v-icon v-else> mdi-email </v-icon>
      </v-btn>
    </template>
    <div class="notifications-container">
      <h2>Notifications</h2>
      <hr color="#bbb" />
      <v-list v-if="$store.state.numOfUnreadNotifications" two-line>
        <v-list-item
          v-for="unreadNotification of $store.state.unreadNotifications"
          :key="unreadNotification.id"
        >
          <v-list-item-content>
            <v-list-item-title>
              <a @click="readNotification(unreadNotification)">
                {{ unreadNotification.question.title }}
              </a>
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ messageText(unreadNotification) }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <div v-else>
        <span>You are up to date!</span>
      </div>
    </div>
  </v-menu>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { Notification } from '~/pages/questions/question.model'

@Component
export default class NotificationMenu extends Vue {
  async readNotification(unreadNotification: Notification) {
    await this.$axios.get(
      '/notifications/' + unreadNotification.id + '/?read=true'
    )
    this.$store.dispatch('getNotifications')
    this.$router.push('/questions/' + unreadNotification.question.id)
  }

  messageText(notification: Notification): string {
    let message = ''
    message += notification.answers > 0 ? `${notification.answers} answer` : ''
    message += notification.answers > 1 ? 's' : ''
    message += notification.answers && notification.comments ? ' and ' : ''
    message +=
      notification.comments > 0 ? `${notification.comments} comment` : ''
    message += notification.comments > 1 ? 's' : ''
    return message
  }

  created() {
    this.$store.dispatch('getNotifications')
  }
}
</script>

<style scoped>
.notifications-container {
  background-color: white;
  width: 250px;
  padding: 10px;
}

.v-list-item,
.v-list {
  padding: 0;
}
</style>
