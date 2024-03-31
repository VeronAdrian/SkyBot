package com.example.sky_weatherchatbot.ui

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import androidx.activity.compose.setContent
import androidx.appcompat.app.AppCompatActivity
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.biometric.BiometricPrompt.AuthenticationResult
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.sky_weatherchatbot.ui.theme.SkyWeatherChatbotTheme



class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SkyWeatherChatbotTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Auth()
                }
            }
        }
        setUpAuth()
    }

    //------------------------Login-------------------------//
    private var canAuthenticate = false
    private lateinit var promptInfo: BiometricPrompt.PromptInfo

    @SuppressLint("SuspiciousIndentation")
    private fun setUpAuth(){
        if (BiometricManager.from(this).canAuthenticate(BiometricManager.Authenticators.BIOMETRIC_STRONG
                    or BiometricManager.Authenticators.DEVICE_CREDENTIAL) == BiometricManager.BIOMETRIC_SUCCESS)
            canAuthenticate = true
            promptInfo = BiometricPrompt.PromptInfo.Builder()
                .setTitle("Biometric Authentication")
                .setSubtitle("Authenticate using the biometric sensor")
                .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_STRONG
                        or BiometricManager.Authenticators.DEVICE_CREDENTIAL)
                .build()
    }

    private fun authenticate(auth: (auth: Boolean) -> Unit){
        if (canAuthenticate){
            BiometricPrompt(this, ContextCompat.getMainExecutor(this),
                object: BiometricPrompt.AuthenticationCallback(){
                    override fun onAuthenticationSucceeded(result: AuthenticationResult) {
                        super.onAuthenticationSucceeded(result)
                        auth(true)
                    }
                }).authenticate(promptInfo)
        }
        else{
            auth(true)
        }
    }

    @Composable
    fun Auth() {

        var auth by remember { mutableStateOf(false) }

        Column (modifier = Modifier
            .background(if (auth)Color.White else Color.DarkGray)
            .fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(if (auth)"You are authenticated" else "You need to authenticate", fontSize = 22.sp, fontWeight = FontWeight.Bold )
            Spacer(modifier = Modifier.height(8.dp))

            Button(onClick = {
                if (auth){
                    val intent = Intent(this@MainActivity, Chat::class.java)
                    startActivity(intent)
                }
                else{
                    authenticate { auth = it }
                }
            }) {
                Text(if (auth) "Start Chatting" else "Authenticate")
            }
        }
    }
    //------------------------------------------------------//
    /*
    @Preview(showSystemUi = true)
    @Composable
    fun DefaultPreview() {
        SkyWeatherChatbotTheme {
            Auth()
        }
    }*/
}

