package com.example.sky_weatherchatbot.model
import com.example.sky_weatherchatbot.R
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView


class MessageAdapter(private val messages: MutableList<Message>) : RecyclerView.Adapter<MessageAdapter.MessageViewHolder>() {

    class MessageViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val inMessage: TextView = view.findViewById(R.id.in_message)
        val outMessage: TextView = view.findViewById(R.id.out_message)
    }


    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MessageViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.message_item, parent, false)
        return MessageViewHolder(view)
    }

    override fun onBindViewHolder(holder: MessageViewHolder, position: Int) {
        val message = messages[position]
        if (message.isFromUser) {
            holder.inMessage.text = message.text
            holder.inMessage.visibility = View.VISIBLE
            holder.outMessage.visibility = View.GONE
        } else {
            holder.outMessage.text = message.text
            holder.outMessage.visibility = View.VISIBLE
            holder.inMessage.visibility = View.GONE
        }
    }


    override fun getItemCount() = messages.size

    fun addMessage(message: Message) {
        messages.add(message)
        notifyItemInserted(messages.size - 1)
    }

}