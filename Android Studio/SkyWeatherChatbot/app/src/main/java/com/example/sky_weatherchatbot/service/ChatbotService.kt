package com.example.sky_weatherchatbot.service
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.sky_weatherchatbot.R
import com.example.sky_weatherchatbot.model.Message
import com.example.sky_weatherchatbot.model.MessageAdapter

class ChatbotService(private val messageAdapter: MessageAdapter) {
    fun sendWelcomeMessage(){
        val message = Message("Sky: ¡Hola! Soy tu asistente de clima. ¿En qué ciudad quieres saber el clima?:", false)
        messageAdapter.addMessage(message)
    }
    fun sendMessage(messageText: String) {

        if (messageText.isNotEmpty()) {
            val message = Message(messageText, true) // Asumiendo que el mensaje es del usuario
            messageAdapter.addMessage(message)

            val list = mutableListOf<Message>()
            list.add(Message("Sky: ¡Hola! Soy tu asistente de clima. ¿En qué ciudad quieres saber el clima?:", false))
            // Simulación de una respuesta del chatbot
            list.forEach { chatbotMessage ->
                messageAdapter.addMessage(chatbotMessage)
            }
        }
    }
}