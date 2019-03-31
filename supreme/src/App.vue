<template>
  <div>
     <nav class="navbar navbar-expand-md navbar-dark bg-dark">
      <a class="navbar-brand" href="#">vSupreme</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar" aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbar">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item" v-for="item in navitems" v-bind:key="item.path">
            <router-link class="nav-link" :to="item.path">{{ item.component }}</router-link>
          </li>
        </ul>
      </div>
    </nav>
    <transition name="fade" mode="out-in" :duration="100">
      <router-view/>
    </transition>
  </div>
</template>

<script>
import { routerOptions } from "@/variables.js"

export default {
  name: 'App',
  data() {
    return {
      navitems: routerOptions
    };
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  @font-face {
    font-family: "vSupreme";
    src: url("assets/FuturaStd-HeavyOblique.otf");
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: 'vSupreme' !important;
  }

  .users, .groups, .hosts {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }

  .users .page-header, .groups .page-header, .hosts .page-header {
    margin: 0 1rem 1rem 1rem;
  }

  a.navbar-brand {
    font-family: vSupreme;
    background-color: red;
    font-size: 2em;
    padding: .2em;
  }

  .card {
    margin: 0.5rem;
    width: 100%;
  }

  .container {
    padding: 1em;
  }

  .actions a {
    color: white !important;
    margin-left: 5px;
  }

  .fade-enter-active, .fade-leave-active {
    transition: all 1s;
  }

  .fade-enter, .fade-leave-to {
    opacity: 0;
  }

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
</style>
