<template>
  <div class="container">
    <div class="row">
      <b-container fluid class="bv-example-row">
        <b-row>
          <b-col sm="9">
            Level 1: sm="9"
          <b-row>
          <b-col cols="8" sm="6">Level 2: cols="8" sm="6"</b-col>
          <b-col cols="4" sm="6">Level 2: cols="4" sm="6"</b-col>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</div class="row">
    <div class="row">
      <div class="col-sm-10">
        <h1>Hosts</h1>
        <hr><br><br>
        <b-alert v-model="showDismissibleAlert" variant="success" dismissible>
          {{ message }}
        </b-alert>
        <div v-if="hosts.length < 1">
          <b-alert variant="warning" show>
            You need to add a device.
          </b-alert>
	</div>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.Host-modal>Add Host</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">IP Address</th>
              <th scope="col">Computer Name</th>
              <th scope="col">MinKNOW Version</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(host, index) in hosts" :key="index">
              <td>{{ host.ipaddress }}</td>
              <td>{{ host.computer_name }}</td>
              <td>
                <span v-if="host.minknow_version">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.edit-Host-modal
                    @click="editHost(host)">
                    Update
                  </button>
                  <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="onDeleteHost(host)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addHostModal"
            id="Host-modal"
            title="Add a new Host"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-ipaddress-group"
                    label="IP Address:"
                    label-for="form-ipaddress-input">
          <b-form-input id="form-ipaddress-input"
                        type="text"
                        v-model="addHostForm.ipaddress"
                        required
                        placeholder="Enter IP Address">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-computer_name-group"
                      label="Computer Name:"
                      label-for="form-computer_name-input">
            <b-form-input id="form-computer_name-input"
                          type="text"
                          v-model="addHostForm.computer_name"
                          placeholder="Enter Computer Name">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-minknow_version-group">
          <b-form-checkbox-group v-model="addHostForm.minknow_version" id="form-checks">
            <b-form-checkbox value="true">MinKNOW Version?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  <b-modal ref="editHostModal"
         id="edit-Host-modal"
         title="Update"
         hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
  <b-form-group id="form-title-edit-group"
                label="IP Address:"
                label-for="form-ipaddress-edit-input">
      <b-form-input id="form-ipaddress-edit-input"
                    type="text"
                    v-model="editHostForm.ipaddress"
                    required
                    placeholder="Enter IP Address">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-computer_name-edit-group"
                  label="Computer Name:"
                  label-for="form-computer_name-edit-input">
        <b-form-input id="form-computer_name-edit-input"
                      type="text"
                      v-model="editHostForm.computer_name"
                      required
                      placeholder="Enter Computer Name">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-minknow_version-edit-group">
      <b-form-checkbox-group v-model="editHostForm.minknow_version" id="edit-form-checks">
        <b-form-checkbox value="true">MinKNOW Version?</b-form-checkbox>
      </b-form-checkbox-group>
    </b-form-group>
    <b-button-group>
      <b-button type="submit" variant="primary">Update</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-button-group>
  </b-form>
</b-modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      showDismissibleAlert: false,
      hosts: [],
      addHostForm: {
        ipaddress: '',
        computer_name: '',
        minknow_version: [],
      },
      editHostForm: {
        id: '',
        ipaddress: '',
        computer_name: '',
        minknow_version: [],
      },
      message: '',
    };
  },
  methods: {
    editHost(host) {
      this.editForm = host;
    },
    getHosts() {
      const path = 'http://192.168.1.68:5000/hosts';
      axios.get(path)
        .then((res) => {
          this.hosts = res.data.hosts;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addHost(payload) {
      const path = 'http://192.168.1.68:5000/hosts';
      axios.post(path, payload)
        .then(() => {
          this.getHosts();
          this.message = 'Host added!';
          this.showDismissibleAlert = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getHosts();
        });
    },
    initForm() {
      this.addHostForm.ipaddress = '';
      this.addHostForm.computer_name = '';
      this.addHostForm.minknow_version = [];
      this.editHostForm.id = '';
      this.editHostForm.ipaddress = '';
      this.editHostForm.computer_name = '';
      this.editHostForm.minknow_version = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addHostModal.hide();
      let addminknowversion = false;
      if (this.addHostForm.minknow_version[0]) addminknowversion = true;
      const payload = {
        ipaddress: this.addHostForm.ipaddress,
        computer_name: this.addHostForm.computer_name,
        addminknowversion, // property shorthand
      };
      this.addHost(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addHostModal.hide();
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editHostModal.hide();
      let editminknowversion = false;
      if (this.editHostForm.minknow_version[0]) editminknowversion = true;
      const payload = {
        ipaddress: this.editHostForm.ipaddress,
        computer_name: this.editHostForm.computer_name,
        editminknowversion, // property shorthand
      };
      this.updateHost(payload, this.editForm.id);
    },
    updateHost(payload, hostID) {
    const path = `http://192.168.1.68:5000/hosts/${hostID}`;
    axios.put(path, payload)
      .then(() => {
        this.getHosts();
        this.message = 'Host updated!';
        this.showDismissibleAlert = true;
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getHosts();
      });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editHostModal.hide();
      this.initForm();
      this.getHosts(); // why?
    },
    removeHost(hostID) {
    const path = `http://192.168.1.68:5000/hosts/${hostID}`;
    axios.delete(path)
      .then(() => {
        this.getHosts();
        this.message = 'Host removed!';
        this.showDismissibleAlert = true;
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getHosts();
      });
    },
    onDeleteHost(host) {
      this.removeHost(host.id);
    },
  },
  created() {
    this.getHosts();
    setInterval(() => this.getHosts(),1000);
  },
};
</script>
