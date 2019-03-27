<template>
  <div>
     <nav class="navbar navbar-expand-md navbar-dark bg-dark">
      <a class="navbar-brand" href="#">vSupreme</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar" aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbar">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Users</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/groups">Groups</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/hosts">Hosts</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/about">About</router-link>
          </li>
        </ul>
      </div>
    </nav>
    <transition name="slide" mode="out-in" :duration="100">
      <router-view/>
    </transition>
  </div>
</template>

<style>
  @font-face {
    font-family: "vSupreme";
    src: url("assets/FuturaStd-HeavyOblique.otf");
  }

  a.navbar-brand {
    font-family: vSupreme;
    background-color: red;
    font-size: 2em;
    padding: .2em;
  }

  .container {
    padding: 1em;
  }
</style>
