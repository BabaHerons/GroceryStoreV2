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
    private fetch_patch(json_data:any) {
        return {
            method:'PATCH',
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
                    router.push({path:"/login"})
                } else {
                    localStorage.setItem("user", k.full_name)
                }
            })
        } else {
            localStorage.setItem("global_error", "Access Denied. Please login to continue.")
            router.push({path:"/login"})
        }
    }


    // LOGIN
    public login(json_data:any){
        return fetch(this.BASE_URL + "/login", this.fetch_post(json_data))
    }

    // SIGN UP FORM
    public sign_up(json_data:any){
        return fetch(this.BASE_URL + "/sign-up", this.fetch_post(json_data))
    }

    // OTP FOR COMPLETING SIGN UP
    public sign_up_otp(json_data:any){
        return fetch(this.BASE_URL + "/sign-up", this.fetch_patch(json_data))
    }

    // EMAIL FOR FORGOT PASSWORD
    public send_fp_email(json_data:any){
        return fetch(this.BASE_URL + "/forgot-password", this.fetch_post(json_data))
    }

    // EMAIL FOR FORGOT PASSWORD
    public send_fp_otp_pass(json_data:any){
        return fetch(this.BASE_URL + "/forgot-password", this.fetch_patch(json_data))
    }
}

export default new API