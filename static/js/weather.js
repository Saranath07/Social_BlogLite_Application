home_town = document.querySelector(".h_t")

Vue.component('city',
            
{
    props : ['c'],
    data : function(){
        return {

        }
    },
    template:`
    <div class = "card" style="width: 18rem;">
    <div class="card-body">
        <div class="card-title">{{c.name}}</div>
        <div class="card-text" v-if="!c.err">
            Curret temp : {{c.temp}} Celcius <br />
            Min temp : {{c.temp_min}} Celcius <br />
            Max temp : {{c.temp_max}} Celcius <br />
            Last Updated : {{c.lastUpdate}} <br />
        </div>
        <div class="card-text alert alert-danger" v-else>
            Something went wrong : {{c.errmsg}}
        </div>
        <button class="btn btn-info" @click="update">Update</button>
        <button class="btn btn-danger" @click="remove">Delete</button>
    </div>

</div> 
    `,
    created(){
        Vue.set(this.c, 'temp', 'NA');
        this.c.temp_min = "NA";
        this.c.temp_max = "NA";
        this.c.err = false;
    },
    methods: {
        updateTemp(){
            if(!this.c.err){
                x = this.c.weather.main.temp;
                Vue.set(this.c, 'temp', x ? parseFloat(x-273).toFixed(1) : "NA");
                x = this.c.weather.main.temp_min;
                this.c.temp_min = x ? parseFloat(x - 273).toFixed(1) : "NA";
                x = this.c.weather.main.temp_max;
                this.c.temp_max = x ? parseFloat(x - 273).toFixed(1) : "NA";
            }
        },
        async update(){
            const url = `https://api.openweathermap.org/data/2.5/weather?q=${this.c.name}&appid=6a9c070dae9b37a60371f67e004942ff`
            console.log("Child" + url)
            fetch(url)
                .then((resp) =>{
                    if (resp.status >= 400 && resp.status < 600){
                        this.c.err = true
                        this.c.errmsg = "Don't know how to fetch data"
                        return resp
                    } else {
                        return resp.json()
                    }
                })
            
                .then((data) => {
                    this.c.weather = data
                    this.updateTemp()
                    this.$forceUpdate()
                })
                .catch((err) =>{
                    this.c.err = true
                    this.c.errmsg = "Network error" + err
                })
                this.c.err = false
                this.c.lastUpdate = new Date().toJSON()
        },
        remove(){
            this.$parent.removeCity(this.c.name);
        },
        
    }

})

let app = new Vue({
    el: "#app",
    data:{
        newcity: "",
        
        cities:{home_town: {name: home_town.dataset.home_town}
    
    }},
    methods: {
        addCity(c){
            this.cities[c] = {name : c};
            this.newcity = "";
        },
        removeCity(c){
            delete this.cities[c];
            this.$forceUpdate();
        }
    }
    
})