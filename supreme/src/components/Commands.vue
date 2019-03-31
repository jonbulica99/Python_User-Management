<template>
  <div class="command container">
    <h1 class="page-header">Commands</h1>
    <div class="row">
      <div class="card shadow-sm cmd-card" v-for="command in commands">
        <div class="card-body card-flex">
          <h4 class="card-title">{{ command.name }}</h4>
          <p class="card-text">{{ command.description }}</p>
          <a href="#" class="btn btn-primary float-bottom" v-on:click="confirmRun(command.cmd)">Run</a>
        </div>
      </div>
    </div>
    <br>
    <div class="cmd-progress">
      <h3>Progress</h3>
      <div class="card" v-if="this.progress">
        <div class="card-body">
          <b-progress :value="progress.percent" :max="100" show-progress animated></b-progress>
          <b>Command</b>
          : {{ progress.command }}
          <div v-if="progress.command">
            <p v-if="progress.current.object && progress.current.object.name">
              <b>Status</b>: Working on
              <b>{{ progress.current.object.name }}</b> at host
              <b>{{ progress.current.host.name }}</b>.
            </p>
            <div class="row">
              <div v-if="progress.success.length  " class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">Successful hosts</h5>
                  <div class="card-text">
                    <p v-if="progress.success" v-for="host in progress.success">{{ host.name }}</p>
                  </div>
                </div>
              </div>
              <div v-if="progress.error.length" class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">Failed hosts</h5>
                  <div class="card-text">
                    <p v-if="progress.error" v-for="host in progress.error">{{ host.name }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <i>No command is running at this time.</i>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { EventBus } from "@/events.js";
import { Endpoints } from "@/variables.js";

export default {
  name: "commands",
  data() {
    return {
      command_url: Endpoints.COMMANDS,
      commands: [
        {
          name: "Insert defaults",
          description:
            "Insert the default values into the database. You only have to do this once.",
          cmd: "insert_defaults"
        },
        {
          name: "Deploy everything",
          description:
            "Deploys all defined users and groups to all specified hosts.",
          cmd: "deploy_all"
        },
        {
          name: "Force commit",
          description:
            "Force commit all changes. Note that this is done automatically for all successful actions.",
          cmd: "force_commit"
        },
        {
          name: "Force rollback",
          description: "Rollback all changes since last commit.",
          cmd: "force_rollback"
        }
      ],
      fetch_progress: false,
      progress: null,
      thread_id: null
    };
  },
  methods: {
    confirmRun(command) {
      this.$dialog
        .confirm("Do you really want to run <b>" + command + "</b>?")
        .then(() => {
          this.runCommand(command);
        })
        .catch(() => {
          console.log("Run command aborted.");
        });
    },
    runCommand(command) {
      axios.post(this.command_url + command).then(response => {
        response = response.data;
        if (response.success) {
          this.fetch_progress = true;
          this.thread_id = response.data;
          console.log(
            "Command " +
              command +
              " dispatched successfully. (thread #" +
              this.thread_id +
              ")"
          );
          this.fetchCommandProgress(command);
        } else {
          this.$dialog.alert(
            "<b>Error running command</b>: " +
              response.message +
              "<br><i>Check the console log for more information.</i>"
          );
          console.log(response.exception);
        }
      });
    },
    fetchCommandProgress(command) {
      axios
        .get(this.command_url + command + "?thread=" + this.thread_id)
        .then(response => {
          this.progress = response.data.data;
          if (response.data.success) {
            if (this.progress.percent == 100 && this.progress.current.host == null) {
              this.fetch_progress = false;
              this.$dialog.alert(
                "Command <b>" + command + "</b> completed successfully."
              );
            }
            if (this.fetch_progress) {
              setTimeout(this.fetchCommandProgress(command), 1000);
            }
          } else {
            console.log(response.data.exception);
            if (this.progress.percent == 100 && this.progress.current.host == null) {
              this.$dialog.alert(
                "<b>Error </b>: " +
                  response.data.message +
                  "<br><i>Check the console log for more information.</i>"
              );
            }
          }
        });
    }
  }
};
</script>

<style scoped>
.card {
  margin: 0.5rem;
  width: 100%;
}

.cmd-card {
  width: 18rem;
}

.card-flex {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
}

.float-bottom {
  align-self: flex-end;
}
</style>
