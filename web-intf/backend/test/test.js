const app = require("../app");
const test = require('unit.js');
require('dotenv').config({ path: '../.env' });

describe('Testing /login endpoint', function(){
    it('Login with valid credentials', function(done){
        const user = {
            username: process.env.USERNAME,
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(200, done);

    })

    it('Login with invalid credentials', function(done){
        const user = {
            username: "testuser8000",
            password: "fsfasas"
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })

    it('Login with incorrect username', function(done){
        const user = {
            username: "testuser9000",
            password: "27190670Kendrick#"
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400, "{\"error\":\"User Not Found!\"}",done);


    })

    it('Login with incorrect password', function(done){
        const user = {
            username: "testuser8000",
            password: "fsfasasdF#4"
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(401, "{\"error\":\"Incorrect Password!\"}",done);


    })
})
