/**
  * @brief Add to the debug buffer.
  * 
  * @note Use the macros unless you know what you're doing!
  *
  * @param message A C-string with the message you want to send.
  * @param len The length of the message you want to send.
  * @param log_level The severity of the debug message.
  * 
  * @return The status of the debug module.
  */
DEBUG_STATUS debug_log
    (
    const char* message,
    size_t len,
    DEBUG_LEVEL log_level
    )