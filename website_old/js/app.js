import cors from "cors";
const corsOrigin ={
    origin:'http://localhost:8080', //or whatever port your frontend is using
    credentials:true,            
    optionSuccessStatus:200
}
app.use(cors(corsOrigin));