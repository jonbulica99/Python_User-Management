<template>
  <div class="command container">
    <h1 class="page-header">Commands</h1>
    <div class="row">
      <div class="card shadow-sm cmd-card" v-for="command in commands" :key="command.name">
        <div class="card-body card-flex">
          <h4 class="card-title">{{ command.name }}</h4>
          <p class="card-text">{{ command.description }}</p>
          <button
            class="btn btn-danger float-bottom"
            v-if="progress && progress.command == command.cmd && progress.percent < 100"
            @click="cancelCommand(command.cmd)"
          >Cancel</button>
          <button class="btn btn-primary float-bottom" @click="confirmRun(command.cmd)" v-else>Run</button>
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
            <p v-if="progress.current && progress.current.object && progress.current.object.name">
              <b>Status</b>: Working on
              <b>{{ progress.current.object.name }}</b> at host
              <b>{{ progress.current.host.name }}</b>.
            </p>
            <div class="row">
              <div v-if="progress.success && progress.success.length" class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">Successful hosts</h5>
                  <div class="card-text">
                    <p v-for="host in progress.success" :key="host.id">{{ host.name }}</p>
                  </div>
                </div>
              </div>
              <div v-if="progress.error && progress.error.length" class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">Failed hosts</h5>
                  <div class="card-text">
                    <p v-for="host in progress.error" :key="host.id">{{ host.name }}</p>
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
      this.progress = null;
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
        if (response.data.success) {
          this.fetch_progress = true;
          console.log("Command " + command + " dispatched successfully.");
          if (command == "deploy_all") {
            this.thread_id = response.data.data;
            console.log("Server using thread #" + this.thread_id);
          }
          this.fetchCommandProgress(command, this.thread_id);
        } else {
          this.commandError(response);
        }
      });
    },
    fetchCommandProgress(command, thread_id) {
      axios
        .get(
          this.command_url + command + (thread_id ? "?thread=" + thread_id : "")
        )
        .then(response => {
          this.progress = response.data.data;

          if (thread_id) {
            if (
              this.progress.percent == 100 &&
              this.progress.current.host == null
            ) {
              if (response.data.success) {
                this.commandSuccess(command);
              } else {
                this.commandError(response);
              }
            }
          } else if (this.progress.percent == 100) {
            if (response.data.success) {
              this.commandSuccess(command);
            } else {
              this.commandError(response);
            }
          }
          if (this.fetch_progress) {
            setTimeout(this.fetchCommandProgress(command, thread_id), 1000);
          }
        });
    },
    commandSuccess(command) {
      this.fetch_progress = false;
      this.$dialog.alert(
        "Command <b>" + command + "</b> completed successfully."
      );
    },
    commandError(response) {
      this.fetch_progress = false;
      if (response.data.exception) {
        console.log(response.data.exception);
      }
      this.$dialog.alert(
        "<b>Error </b>: " +
          response.data.message +
          "<br><i>Check the console log for more information.</i>"
      );
    },
    cancelCommand(command) {
      this.fetch_progress = false;
      this.thread_id = null;
      setTimeout(() => {
        this.progress = null;
        console.log("Command " + command + " cancelled by user.");
      }, 1000);
      /* TODO: implement this functionality on the backend as well. */
      this.$dialog.alert(
        "Command execution <b>" + command + "</b> cancelled by user."
      );
    }
  }
};
</script>

<style scoped>
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
