# Project Structure

\---GroceryStoreV2
    |   .gitignore
    |   
    +---backend
    |   |   dump.rdb
    |   |   main.py
    |   |   requirements.txt
    |   |   
    |   +---instance
    |   |       grocery_store_v2.db
    |   |       
    |   \---src
    |       |   custom_cache.py
    |       |   jwt.py
    |       |   models.py
    |       |   tasks.py
    |       |   utils.py
    |       |   __init__.py
    |       |   
    |       +---exports
    |       |       products.csv
    |       |       
    |       +---routes
    |       |       auth.py
    |       |       cart.py
    |       |       category.py
    |       |       order.py
    |       |       product.py
    |       |       summary.py
    |       |       test.py
    |       |       user.py
    |       |       
    |       +---sales_report
    |       |       category.png
    |       |       products.png
    |       |       
    |       \---templates
    |               forgot_pass.html
    |               invoice.html
    |               monthly_report.html
    |               reminder.html
    |               reminder_cart.html
    |               signup_pass.html
    |               
    \---frontend
        |   .gitignore
        |   index.html
        |   package-lock.json
        |   package.json
        |   README.md
        |   tsconfig.json
        |   tsconfig.node.json
        |   vite.config.ts
        |   
        +---.vscode
        |       extensions.json
        |       
        +---public
        |       vite.svg
        |       
        \---src
            |   api.ts
            |   App.vue
            |   main.ts
            |   router.ts
            |   style.css
            |   vite-env.d.ts
            |   
            +---assets
            |       vue.svg
            |       
            +---components
            |       AdminDash.vue
            |       Navbar.vue
            |       SMDash.vue
            |       UserDash.vue
            |       
            \---pages
                    Dashboard.vue
                    Home.vue
                    Login.vue
                    
