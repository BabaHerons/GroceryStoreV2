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
    private fetch_delete(json_data:any = {}) {
        return {
            method:'DELETE',
            headers: {
                "Content-Type": "application/json",
                "token": `${localStorage.getItem("token")}`,
                "role": `${localStorage.getItem("role")}`,
                "user-id": `${localStorage.getItem("user_id")}`
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
                    console.log(k);
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


    // ------------------------LOGIN----------------------------------
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
    // ---------------------------------------------------------------

    
    // ------------------------USERS----------------------------------
    // USERS
    public get_users(){
        return fetch(this.BASE_URL + "/users", this.fetch_get())
    }

    // STORE/INVENTORY MANAGER ACTIVATION
    public activate_manager(json_data:any){
        return fetch(this.BASE_URL + "/users", this.fetch_patch(json_data))
    }
    // ----------------------------------------------------------------


    // ------------------------CATEGORY----------------------------------
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
    // -------------------------------------------------------------------


    // ------------------------CATEGORY CHANGE REQUEST--------------------
    // GET ALL CATEGORIES REQUESTS
    public get_categories_request(){
        return fetch(this.BASE_URL + "/category-request", this.fetch_get())
    }

    // ADD A CATEGORY REQIUEST
    public post_category_request(json_data:any){
        return fetch(this.BASE_URL + "/category-request", this.fetch_post(json_data))
    }

    // RESPOND TO CATEGORY REQIUEST EDIT
    public patch_category_request(json_data:any){
        return fetch(this.BASE_URL + "/category-request", this.fetch_patch(json_data))
    }

    // RESPOND TO CATEGORY REQIUEST DELETE
    public delete_category_request(json_data:any){
        return fetch(this.BASE_URL + "/category-request", this.fetch_delete(json_data))
    }
    // -------------------------------------------------------------------


    // -------------------------PRODUCT------------------------------------
    // GET ALL PRODUCTS
    public get_all_products(){
        return fetch(this.BASE_URL + "/products", this.fetch_get())
    }

    // CREATE A PRODUCT
    public post_product(json_data:any){
        return fetch(this.BASE_URL + "/products", this.fetch_post(json_data))
    }

    // EDIT A PRODUCT
    public put_product(json_data:any){
        return fetch(this.BASE_URL + "/products", this.fetch_put(json_data))
    }

    // DELETE A PRODUCT
    public delete_product(id:any){
        return fetch(this.BASE_URL + `/products?id=${id}`, this.fetch_delete())
    }
    // -------------------------------------------------------------------


    // -------------------------CART--------------------------------------
    // GET CART
    public get_cart(){
        return fetch(this.BASE_URL + "/cart", this.fetch_get())
    }

    // ADD TO CART
    public post_cart(json_data:any){
        return fetch(this.BASE_URL + "/cart", this.fetch_post(json_data))
    }

    // UPDATE QUANTITY TO PURCHASE IN CART
    public patch_cart(json_data:any, id:any){
        return fetch(this.BASE_URL + `/cart?id=${id}`, this.fetch_patch(json_data))
    }

    // REMOVE ITEM FROM CART
    public delete_item_from_cart(id:any){
        return fetch(this.BASE_URL + `/cart?id=${id}`, this.fetch_delete())
    }
    // -------------------------------------------------------------------


    // --------------------------ORDER------------------------------------
    // GET ALL ORDERS
    public get_orders(){
        return fetch(this.BASE_URL + "/orders", this.fetch_get())
    }

    // CREATE AN ORDER
    public post_order(json_data:any){
        return fetch(this.BASE_URL + "/orders", this.fetch_post(json_data))
    }
    // -------------------------------------------------------------------


    // --------------------------SEND INVOICE ON MAIL---------------------
    public send_invoice_email(order_id:any){
        return fetch(this.BASE_URL + `/invoice/${order_id}`, this.fetch_get())
    }
    // -------------------------------------------------------------------


    // --------------------------EXPORT PRODUCTS CSV----------------------
    public export_products_csv(){
        return fetch(this.BASE_URL + '/products/csv', this.fetch_get())
    }
    // -------------------------------------------------------------------

    
    // --------------------------MONTHLY SALES REPORT----------------------
    public monthly_sales_report_products(){
        return fetch(this.BASE_URL + '/monthly-sales-report/products', this.fetch_get())
    }

    public monthly_sales_report_category(){
        return fetch(this.BASE_URL + '/monthly-sales-report/category', this.fetch_get())
    }
    // -------------------------------------------------------------------

}

export default new API