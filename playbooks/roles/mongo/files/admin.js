admin = db.getSiblingDB("admin")
admin.createUser(
  {
    user: "admin",
    pwd: "adminPassword2018",
    roles: [ { role: "root", db: "admin" } ]
  }
)

// db.getSiblingDB("admin").auth("admin", "adminPassword2018" )

// db.getSiblingDB("admin").createUser(
//   {
//     "user" : "replicaAdmin",
//     "pwd" : "replicaAdminPassword2018",
//     roles: [ { "role" : "clusterAdmin", "db" : "admin" } ]
//   }
// )