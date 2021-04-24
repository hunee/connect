/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 2; tab-width: 2 -*- */

#pragma once

#include <memory>
#include <iostream>


/**
 * @brief 
 * 
 * @tparam T 
 */
template <typename T>
class unique_ptr {
protected:
    unique_ptr() {}

public:
    virtual ~unique_ptr() {}

public:

    /**
     * @brief 
     * 
     * @return T* 
     */
    static T * get()
    {
        if (unique_ptr_ == nullptr)
            unique_ptr_ = std::make_unique<T>();

        return unique_ptr_.get();
    }

    /**
     * @brief 
     * 
     */
    static void reset()
    {
        if (unique_ptr_ != nullptr)
            unique_ptr_.reset(nullptr);
    }

private:
    // This version just uses delete to destroy the pointer.
    static std::unique_ptr<T> unique_ptr_;
};


/**
 * @brief 
 * 
 * @tparam T 
 */
template <typename T>
std::unique_ptr<T> unique_ptr<T>::unique_ptr_ = nullptr;

