import router from "./router.ts";

class API{
    private BASE_URL = "http://localhost:5000"
    private fetch_get() {
        return {
            method:'GET',
            headers: {
                "token": `${localStorage.getItem("token")}`,
                "role": `${localStorage.getItem("role")}`,
                "user-id": `${localStorage.getItem("user_id")}`
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
                "user-id": `${localStorage.getItem("user_id")}`
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
                "user-id": `${localStorage.getItem("user_id")}`
            },
            body:JSON.stringify(json_data)
        }
    }
    private fetch_put(json_data:any) {
        return {
            method:'PUT',
            headers: {
                "Content-Type": "application/json",
                "token": `${localStorage.getItem("token")}`,
                "role": `${localStorage.getItem("role")}`,
                "user-id": `${localStorage.getItem("user_id")}`
            },
            body:JSON.stringify(json_data)
        }
    }
    private fetch_delete() {
        return {
            method:'DELETE',
            headers: {
                "token": `${localStorage.getItem("token")}`,
                "role": `${localStorage.getItem("role")}`,
                "user-id": `${localStorage.getItem("user_id")}`
            }
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
                    localStorage.removeItem("user_id")
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

    // CREATE NEW PASSWORD
    public send_fp_otp_pass(json_data:any){
        return fetch(this.BASE_URL + "/forgot-password", this.fetch_patch(json_data))
    }

    // USERS
    public get_users(){
        return fetch(this.BASE_URL + "/users", this.fetch_get())
    }

    // STORE/INVENTORY MANAGER ACTIVATION
    public activate_manager(json_data:any){
        return fetch(this.BASE_URL + "/users", this.fetch_patch(json_data))
    }

    // GET ALL CATEGORIES
    public get_categories(){
        return fetch(this.BASE_URL + "/category", this.fetch_get())
    }

    // GET A CATEGORY
    public get_category(id:any){
        return fetch(this.BASE_URL + `/category?id=${id}`, this.fetch_get())
    }

    // CREATE A CATEGORY
    public post_category(json_data:any){
        return fetch(this.BASE_URL + "/category", this.fetch_post(json_data))
    }

    // EDIT A CATEGORY
    public put_category(json_data:any){
        return fetch(this.BASE_URL + "/category", this.fetch_put(json_data))
    }

    // APROOVE A CATEGORY
    public patch_category_approve(id:any, json_data:any = null){
        return fetch(this.BASE_URL + `/category?id=${id}`, this.fetch_patch(json_data))
    }

    // DELETE A CATEGORY
    public delete_category(id:any){
        return fetch(this.BASE_URL + `/category?id=${id}`, this.fetch_delete())
    }
}

export default new API