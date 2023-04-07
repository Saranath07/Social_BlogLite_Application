

Vue.component('register',
            
{
    
    data : function(){
        return {
            form: {
              email: "",
              password: "",
              confirmPassword: ""
            }
          };
        },
        
    template:`
    
    <div>
    <style>
.is-invalid {
  border-color: red;
}
</style>
    <h2>Register</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="form.email" />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="form.password" />
        <p v-if="passwordStrength < 50" class="text-danger">
          Weak password
        </p>
        <p v-else-if="passwordStrength >= 50 && passwordStrength < 80" class="text-warning">
          Good password
        </p>
        <p v-else class="text-success">
          Strong password
        </p>
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password:</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="form.confirmPassword"
          :class="{ 'is-invalid': form.confirmPassword !== form.password }"
        />
        <p v-if="form.confirmPassword !== form.password" class="text-danger">
          Passwords do not match
        </p>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
    `,
    created(){
        Vue.set(this.c, 'temp', 'NA');
        this.c.temp_min = "NA";
        this.c.temp_max = "NA";
        this.c.err = false;
    },
    computed: {
        passwordStrength() {
          let strength = 0;
          if (this.form.password.length >= 6) {
            strength += 20;
          }
          if (this.form.password.match(/[a-z]+/)) {
            strength += 20;
          }
          if (this.form.password.match(/[A-Z]+/)) {
            strength += 20;
          }
          if (this.form.password.match(/[0-9]+/)) {
            strength += 20;
          }
          if (this.form.password.match(/[!@#\$%\^&\*]+/)) {
            strength += 20;
          }
          return strength;
        }
      },
      methods: {
        submitForm() {
          if (this.form.password === this.form.confirmPassword) {
            console.log("Submitting form");
            // Add your form submit logic here
          }
        }
      }
    }
    

)

let app = new Vue({
    el: "#app",
    data:{
        
            email: "",
            password: "",
            confirmPassword: ""
    },
    methods: {
        submitForm() {
          if (this.form.password === this.form.confirmPassword) {
            console.log("Submitting form");
            // Add your form submit logic here
          }
        }
      }
    })