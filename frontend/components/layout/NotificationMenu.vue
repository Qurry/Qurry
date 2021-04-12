<template>
  <v-menu offset-y>
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon v-bind="attrs" v-on="on">
        <v-badge color="secondary" content="6">
          <v-icon> mdi-email </v-icon>
        </v-badge>
      </v-btn>
    </template>
    <v-list two-line>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Answer</v-list-item-title>
          <v-list-item-subtitle>
            Was genau ist ein Graph?
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Comment</v-list-item-title>
          <v-list-item-subtitle>
            Findet CR dieses Jahr statt?
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
