import com.typesafe.config.ConfigFactory

object ConfigManager {

  private val config = ConfigFactory.load("application.conf")

  def getStreamInput: String = config.getString("Stream.input")
  def getApiUrl: String = config.getString("API.url")
  def getApiOutput: String = config.getString("API.output")

  def getInputStream = config.getString("Stream.input")
  def getCheckpointPath = config.getString("Stream.checkpoint")
  def getSinkPath = config.getString("Stream.sink")

  def getCloudInputStream: String = config.getString("CLOUD-STORAGE.input")
  def getCloudCheckpointPath = config.getString("CLOUD-STORAGE.checkpoint")
  def getCloudSinkPath = config.getString("CLOUD-STORAGE.sink")

  def getAccesKey = config.getString("AWS.accessKey")
  def getAwsSecret = config.getString("AWS.secret")


}
