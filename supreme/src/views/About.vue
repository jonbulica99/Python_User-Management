<template>
  <div class="about container">
    <h1>About</h1>
    <br>
    <div class="card shadow-sm fast-transition">
      <div class="logo card-img-top">vSupreme</div>
      <div class="card-header">General</div>
      <div class="card-body">
        <p>
          <b>vSupreme</b> was created by {{ authors.jonbulica.name }}
          (<a target="_blank" v-bind:href="github_url + authors.jonbulica.handle">@{{ authors.jonbulica.handle }}</a>)
          and {{ authors.robertkeitel.name }}
          (<a target="_blank" v-bind:href="github_url + authors.robertkeitel.handle">@{{ authors.robertkeitel.handle }}</a>)
          as part of a school project in which we had to deploy a list of users and groups from a database into 
          (multiple) UNIX-based hosts.
        </p>
        <p>This is the frontend to that project, because inserting stuff using phpMyAdmin sucks as soon as you have more than 
        one table. Moreover we wanted greater flexibility, a nice UI, and useful error messages.</p>
        <p>
          The fronted was written in <a href="https://vuejs.org/" target="_blank">Vue.js</a> 
          and it uses <a href="https://getbootstrap.com/" target="_blank">Bootstrap 4</a> (with small changes) for styling 
          everything.
        </p>
        <p><i>It is also worth mentioning that this is our very first vue project.</i></p>
      </div>
    </div>
    <br>
    <div class="card shadow-sm fast-transition">
    <div class="card-header">Source code</div>
      <div class="card-body">
        The source code of this project is available on 
        <a v-bind:href="github_url + authors.jonbulica.handle + '/Python_User-Management'" target="_blank">Github</a>.
      </div>
    </div>
    <br>
    <div class="card shadow-sm fast-transition">
      <div class="card-header">Additional information</div>
      <div class="card-body console-font">
        <table>
          <tbody>
            <tr>
              <th>vSupreme version:</th>
              <td>{{ app_version }}</td>
            </tr>
            <tr>
              <th>Vue.js version:</th>
              <td>{{ vue_version }}</td>
            </tr>
            <tr>
              <th>Environment:</th>
              <td>{{ environment }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer">Thanks for using vSupreme!</div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import { PACKAGE, GITHUB } from "@/variables.js";

export default {
  name: "about",
  data() {
    return {
      app_version: PACKAGE.version,
      vue_version: Vue.version,
      environment: process.env.NODE_ENV,
      github_url: GITHUB,
      authors: {
        jonbulica: {
          name: "Jon Bulica",
          handle: "jonbulica99"
        },
        robertkeitel: {
          name: "Robert Keitel",
          handle: "lilSupreme"
        }
      }
    };
  }
};
</script>

<style scoped>
.logo {
  display: flex;
  color: #fff;
  align-items: center;
  justify-content: center;
  font-family: vSupreme;
  background-color: red;
  font-size: 5rem;
  padding: 1rem;
}

.fast-transition {
  position: relative;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
}

.fast-transition::after {
  content: '';
  position: absolute;
  z-index: -1;
  width: 100%;
  height: 100%;
  opacity: 0;
  border-radius: 5px;
  box-shadow: 0 0 15px 0 rgba(0,0,0,0.2);
  transition: opacity 0.3s ease-in-out;
}

.fast-transition:hover::after {
  opacity: 1;
}

.console-font {
  font-family: "Lucida Console", "Lucida Sans Typewriter", monaco, "Bitstream Vera Sans Mono", monospace;
}

.card-footer {
  font-size: 12px;
}
</style>
