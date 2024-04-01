package com.example.sky_weatherchatbot.ui
import com.example.sky_weatherchatbot.R
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.sky_weatherchatbot.model.MessageAdapter
import com.example.sky_weatherchatbot.service.ChatbotService

class Chatbot : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.chat)

        val btnSend = findViewById<Button>(R.id.btn_send)
        val editTextMessage = findViewById<EditText>(R.id.et_message)
        val recyclerView = findViewById<RecyclerView>(R.id.rv_messages)
        val messageAdapter = MessageAdapter(mutableListOf())
        recyclerView.adapter = messageAdapter
        recyclerView.layoutManager = LinearLayoutManager(this)
        val chatbotService = ChatbotService(messageAdapter)
        chatbotService.sendWelcomeMessage()

        btnSend.setOnClickListener {
            val messageText = editTextMessage.text.toString()
            chatbotService.sendMessage(messageText) // Llama al método del servicio
            editTextMessage.text.clear() // Limpia el EditText después de enviar el mensaje
        }

    }

}
