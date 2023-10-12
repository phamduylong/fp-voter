const app = require("../app");
const test = require('unit.js');
const jwt = require("jsonwebtoken");
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
    it('Login with whitespace character exist in username', function(done){
        const user = {
            username: "random User",
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Login with number starts first in username', function(done){
        const user = {
            username: "random User",
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Login with username too short', function(done){
        const user = {
            username: "ran",
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Login with username too long', function(done){
        const user = {
            username: "randomUsernameabc123def456",
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })

    it('Login with password too short', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const user = {
            username: randomUsername,
            password: "Abc123#"
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Login with password too long', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const randomPassword = Math.random().toString(36).slice(2, 25);
        const user = {
            username: randomUsername,
            password: randomPassword
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Login with number in password missing', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const user = {
            username: randomUsername,
            password: "Abc###abc"
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Login with special character in password missing', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const user = {
            username: randomUsername,
            password: "Abcabc123"
        }
        test.httpAgent(app)
            .post('/login')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Login with capital letter in password missing', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const user = {
            username: randomUsername,
            password: "abcabc123##"
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

describe('Testing /register endpoint', function(){
    it('Register with valid credentials', function(done){
        const randomUsername = "a" + Math.random().toString(36).slice(2, 10);

        const user = {
            username: randomUsername,
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(200, done);

    })
    it('Register with whitespace character exist in username', function(done){
        const user = {
            username: "random User",
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Register with number starts first in username', function(done){
        const user = {
            username: "random User",
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Register with username too short', function(done){
        const user = {
            username: "ran",
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Register with username too long', function(done){
        const user = {
            username: "randomUsernameabc123def456",
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Register with password length too short', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const user = {
            username: randomUsername,
            password: "Abc123#"
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Register with password length too long', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const randomPassword = Math.random().toString(36).slice(2, 25);
        const user = {
            username: randomUsername,
            password: randomPassword
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Register with number in password missing', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const user = {
            username: randomUsername,
            password: "Abc###abc"
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Register with special character in password missing', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const user = {
            username: randomUsername,
            password: "Abcabc123"
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Register with capital letter in password missing', function(done){
        const randomUsername = Math.random().toString(36).slice(2, 10);
        const user = {
            username: randomUsername,
            password: "abcabc123##"
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"Username or password entered does not match pattern required!\"}",done);

    })
    it('Register with duplicate username', function(done){
        const user = {
            username: process.env.USERNAME,
            password: process.env.PASSWORD
        }
        test.httpAgent(app)
            .post('/register')
            .send(user)
            .set("Content-Type", 'application/json')
            .expect(400,"{\"error\":\"User already exists!\"}",done);
    })
})


describe('Testing /id=:id endpoint', function(){
    const token = jwt.sign({ user: process.env.USERNAME }, process.env.JWT_SECRET, { expiresIn: '5s' });
    const invalidToken = jwt.sign({ user: process.env.USERNAME }, process.env.JWT_SECRET, { expiresIn: '0s' });
    it('Get user details with valid credentials', function(done){
        test.httpAgent(app)
            .get('/user/id=1')
            .set("Authorization", `Bearer ${token}`)
            .set("Content-Type", 'application/json')
            .expect(200,done);
    })
    it('Get user details with JWT missing', function(done){
        test.httpAgent(app)
            .get('/user/id=1')
            .set("Content-Type", 'application/json')
            .expect(401, "{\"message\":\"Token not provided\"}",done);
    })
    it('Get user details with invalid JWT', function(done){
        test.httpAgent(app)
            .get('/user/id=1')
            .set("Content-Type", 'application/json')
            .set("Authorization", `Bearer ${invalidToken}`)
            .expect(401, "{\"message\":\"Invalid token\"}",done);
    })
    it('Get user details with negative userID', function(done){
        test.httpAgent(app)
            .get('/user/id=-1')
            .set("Authorization", `Bearer ${token}`)
            .set("Content-Type", 'application/json')
            .expect(400, "{\"error\":\"User id is invalid!\"}",done);
    })
    it('Get user details with userID is missing from the db', function(done){
        test.httpAgent(app)
            .get('/user/id=1000')
            .set("Authorization", `Bearer ${token}`)
            .set("Content-Type", 'application/json')
            .expect(400, "{\"error\":\"User Not Found!\"}",done);
    })
})



