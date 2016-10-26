name := """kabu-java"""

version := "1.0"

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  "mysql" % "mysql-connector-java" % "5.1.39",
  "org.apache.commons" % "commons-io" % "1.3.2",
  "log4j" % "log4j" % "1.2.14",
  "org.apache.thrift" % "libthrift" % "0.9.3"
)

javaOptions in run += "-Xmx4096m"
javaOptions in run += "-Xmn4069m"