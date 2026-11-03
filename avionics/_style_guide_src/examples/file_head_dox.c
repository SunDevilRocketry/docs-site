/**
  ******************************************************************************
  * @file   debug_sdr.h
  * @brief  Interfaces for debugging SDR embedded firmware.
  ******************************************************************************
  * @copyright
  *
  * Copyright (c) 2026 Sun Devil Rocketry.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is covered under the   
  * BSD-3-Clause.                                                          
  *                                                                              
  * https://opensource.org/license/bsd-3-clause
  *
  ******************************************************************************
  @verbatim
  ==============================================================================
                      ##### Debug module features #####
  ==============================================================================
  [..]
  (+) Write to a logging interface
  ******************************************************************************
  @endverbatim
  @dir    debug_sdr
  @brief  Provides a unified debug logging interface across SDR embedded code.
          Built for low-memory/no-dynamic-memory/high-reliability environments.
  
  @section dbg_integ Integration Guide
  The debug module is used by a handful of SDR's projects to provide a
  non-blocking debug writer for embedded boards.

  To integrate the module, you need to provide a write callback to debug_init.
  This write callback should meet the following declaration:
  @code
  void overflow_callback_name(const char*, size_t);
  @endcode
  It also needs to call debug_callback_handler after finishing its write. This
  allows for nonblocking operation of the debug module for performance critical
  devices. If your debug writer is blocking, you can safely call 
  debug_callback_handler before returning control flow to the debug module.

  The module also allows you to overwrite the default behavior if the debug
  buffer overflows. As-is, we clear the buffer and queue up a message indicating
  that it overflowed.

  Finally, we include your project's "main.h" header to allow projects to 
  overwrite our default debug buffer size of 2048 bytes. To do this, simply
  define DEBUG_INTF_BUF_SIZE as the number of bytes you want the buffer to be
  in your header.
  *******************************************************************************/