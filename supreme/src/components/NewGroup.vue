<template>
  <div class="new-group container card shadow-sm">
    <h1 class="page-header">{{ action }} Group</h1>
    <hr>
    <form v-on:submit.prevent="handleGroup()" v-on:reset="resetForm()">
      <div class="form-row">
        <div class="col-md-4 mb-3">
          <label for="groupname">Name</label>
          <input
            type="text"
            class="form-control"
            id="groupname"
            ref="groupname"
            v-model="group.name"
            placeholder="Example"
            required
          >
        </div>
        <div class="col-md-3 mb-3">
          <label for="state">State</label>
          <multiselect
            id="state"
            v-model="stateValue"
            :options="group_states"
            :close-on-select="true"
            placeholder="State"
          ></multiselect>
        </div>
        <div class="col-md-3 mb-3">
          <label for="parent">Parent</label>
          <multiselect
            id="parent"
            v-model="parentValue"
            :options="groups"
            :close-on-select="true"
            track-by="id"
            label="name"
            placeholder="Parent"
          ></multiselect>
        </div>
      </div>
      <button class="btn btn-primary" type="submit">Submit</button>
      <span>&nbsp;</span>
      <button class="btn btn-danger" type="reset">Reset</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { EventBus } from "@/events.js";
import { Endpoints } from "@/variables.js";
import Multiselect from "vue-multiselect";

export default {
  name: "new_group",
  components: {
    Multiselect
  },
  data() {
    return {
      action: "New",
      group: {
        id: 0,
        name: "",
        state: "present",
        parent: ""
      },
      groups: [],
      group_states: ["present", "absent", "inactive"],
      group_url: Endpoints.GROUPS
    };
  },
  mounted() {
    EventBus.$on("editGroup", data => {
      this.action = "Edit";
      this.group = data;
      if (this.$refs.groupname) {
        this.$refs.groupname.focus();
      }
    });
    EventBus.$on("deleteGroup", data => {
      this.action = "Delete";
      this.group = data;
      this.handleGroup();
    });
    EventBus.$on("updateGroups", data => {
      this.groups = data;
    });
  },
  methods: {
    handleGroup() {
      this.group.state = this.stateValue;
      this.group.parent = this.parentValue;

      if (!this.group.name) {
        this.$dialog.alert("Please fill in the group name.");
      } else if (!this.group.state) {
        this.$dialog.alert("Please select a valid group state.");
      } else {
        if (this.action === "New") {
          axios.post(this.group_url + "0", this.group).then(response => {
            response = response.data
            if (response.success) {
              this.$dialog.confirm("Group " + response.data.name + " created successfully.");
              EventBus.$emit("fetchGroups");
            } else {
              this.$dialog.alert("<b>Add operation failed</b>: " + response.message); 
              console.log(response.exception);
            }
          });
        } else if (this.action === "Edit") {
          axios.post(this.group_url + "1", this.group).then(response => {
            response = response.data
            if (response.success) {
              this.$dialog.confirm("Group " + this.group.name + " edited successfully.");
              EventBus.$emit("fetchGroups");
            } else {
              this.$dialog.alert("<b>Edit operation failed</b>: " + response.message); 
              console.log(response.exception);
            }
          });
        } else if (this.action === "Delete") {
          axios.post(this.group_url + "2", this.group).then(response => {
            response = response.data
            if (response.success) {
              this.$dialog.confirm("Group " + this.group.name + " deleted successfully.");
              EventBus.$emit("fetchGroups");
            } else {
              this.$dialog.alert("<b>Delete operation failed</b>: " + response.message); 
              console.log(response.exception);
            }
          });
        }
      }
    },
    resetForm() {
      this.group = {
        id: 0,
        name: "",
        state: "present",
        parent: ""
      };
      this.action = "New";
    }
  },
  computed: {
    stateValue: {
      get() {
        if (this.action === "New") {
          return this.group.state;
        } else {
          return this.group.joins.state;
        }
      },
      set(newVal) {
        if (this.action === "New") {
          this.group.state = newVal;
        } else {
          this.group.joins.state = newVal;
        }
      }
    },
    parentValue: {
      get() {
        if (this.action === "New") {
          return this.group.parent;
        } else {
          return this.group.joins.parent;
        }
      },
      set(newVal) {
        if (this.action === "New") {
          this.group.parent = newVal;
        } else {
          this.group.joins.parent = newVal;
        }
      }
    }
  }
};
</script>

<style scoped>
</style>
