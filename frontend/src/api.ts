import router from "./router.ts";

class API{
    private BASE_URL = "http://localhost:5000"
    private fetch_get() {
        return {
            method:'GET',
            headers: {
                "token": `${localStorage.getItem("token")}`,
                "role": `${localStorage.getItem("role")}`,
            }
        }
    }
    private fetch_post(json_data:any) {
        return {
            method:'POST',
            headers: {
                "Content-Type": "application/json",
                "token": `${localStorage.getItem("token")}`,
                "role": `${localStorage.getItem("role")}`,
            },
            body:JSON.stringify(json_data)
        }
    }


    // VERIFY TOKEN
    public verify_token(){
        let error = false
        if (localStorage.getItem("token")){
            const json_data = {"token": `${localStorage.getItem("token")}`}
            fetch(this.BASE_URL + "/verify_token", this.fetch_post(json_data))
            .then(response => {
                if (response.status != 200){
                    error = true
                }
                return response.json()
            })
            .then(data => {
                const k = data
                if (error){
                    localStorage.removeItem("user")
                    localStorage.removeItem("token")
                    localStorage.removeItem("role")
                    localStorage.setItem("global_error", "Session Expired. Please login to continue.")
                    router.push({path:"/"})
                } else {
                    localStorage.setItem("user", k.full_name)
                }
            })
        } else {
            localStorage.setItem("global_error", "Access Denied. Please login to continue.")
            router.push({path:"/"})
        }
    }


    // LOGIN
    public login(json_data:any){
        return fetch(this.BASE_URL + "/login", this.fetch_post(json_data))
    }
}

export default new API