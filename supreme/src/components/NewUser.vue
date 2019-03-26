<template>
  <div class="new-user container">
    <h1 class="page-header">New User</h1>
    <form v-on:submit="newUser">
      <div class="form-row">
        <div class="col-md-4 mb-3">
          <label for="firstname">First Name</label>
          <input
            type="text"
            class="form-control"
            id="firstname"
            v-model="user.firstname"
            placeholder="Max"
            required
          >
        </div>
        <div class="col-md-4 mb-3">
          <label for="lastname">Last Name</label>
          <input
            type="text"
            class="form-control"
            id="lastname"
            v-model="user.lastname"
            placeholder="Mustermann"
            required
          >
        </div>
      </div>
      <div class="form-row">
        <div class="col-md-4 mb-3">
          <label for="password">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="user.password"
            placeholder="Password"
            required
          >
        </div>
      </div>
      <div class="form-row">
        <div class="col-md-3 mb-3">
          <label for="state">Status</label>
          <select class="form-control custom-select mr-sm-2" id="state" v-model="user.state">
            <option default>present</option>
            <option>absent</option>
            <option>inactive</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label for="pubkey">Public SSH Key</label>
        <textarea
          class="form-control"
          id="pubkey"
          rows="2"
          v-model="user.pubkey"
          placeholder="ssh-rsa AAAAB..."
        ></textarea>
      </div>
      <button class="btn btn-primary" type="submit">Benutzer anlegen</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { Endpoints } from "../variables.js";

export default {
  name: "new_user",
  components: {
    Endpoints
  },
  data() {
    return {
      user: {},
      user_url: Endpoints.USERS
    }
  },
  methods: {
    newUser(event) {
      if (!this.user.firstname || !this.user.lastname) {
        alert("Please fill in first and last name.");
      } else {
        axios
          .post(this.user_url + "new", this.user)
          .then(response => {
            console.log(response.data);
          });
      }
      event.preventDefault();
    }
  }
};
</script>

<style scoped>
</style>
