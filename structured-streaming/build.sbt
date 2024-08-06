ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.13.0"

lazy val root = (project in file("."))
  .settings(
    name := "structured-streaming",
  )
libraryDependencies += "org.apache.spark" %% "spark-core" % "3.3.3"

libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.3.3"

// https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws
libraryDependencies += "org.apache.hadoop" % "hadoop-aws" % "3.3.3" // for s3
// https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-common
libraryDependencies += "org.apache.hadoop" % "hadoop-common" % "3.3.3" // for hadoop configuration

libraryDependencies += "com.typesafe" % "config" % "1.4.3"  // for reading application.conf

libraryDependencies +=  "org.scalaj" %% "scalaj-http" % "2.4.2"

// https://mvnrepository.com/artifact/org.scalatest/scalatest
libraryDependencies += "org.scalatest" %% "scalatest" % "3.2.18" % Test

// https://mvnrepository.com/artifact/org.postgresql/postgresql
libraryDependencies += "org.postgresql" % "postgresql" % "42.7.3"