
#pragma once

#ifndef __MERO_FE_S3_SERVER_S3_CLOVIS_WRITER_H__
#define __MERO_FE_S3_SERVER_S3_CLOVIS_WRITER_H__

#include <memory>
#include <functional>

#include "s3_request_object.h"
#include "s3_clovis_context.h"
#include "s3_asyncop_context_base.h"

class S3ClovisWriterContext : public S3AsyncOpContextBase {
  // Basic Operation context.
  struct s3_clovis_op_context * clovis_op_context;
  bool has_clovis_op_context;

  // Read/Write Operation context.
  struct s3_clovis_rw_op_context clovis_rw_op_context;
  bool has_clovis_rw_op_context;

public:
  S3ClovisWriterContext(std::shared_ptr<S3RequestObject> req, std::function<void()> success_callback, std::function<void()> failed_callback) : S3AsyncOpContextBase(req, success_callback, failed_callback) {
    has_clovis_op_context = false;
    has_clovis_rw_op_context = false;
  }

  ~S3ClovisWriterContext() {
    if (has_clovis_op_context) {
      free_basic_op_ctx(clovis_op_context);
    }
    if (has_clovis_rw_op_context) {
      free_basic_rw_op_ctx(&clovis_rw_op_context);
    }
  }

  void set_clovis_op_ctx(struct s3_clovis_op_context *ctx) {
    clovis_op_context = ctx;
    has_clovis_op_context = true;
  }

  void set_clovis_rw_op_ctx(struct s3_clovis_rw_op_context ctx) {
    clovis_rw_op_context = ctx;
    has_clovis_rw_op_context = true;
  }

};

enum class S3ClovisWriterOpState {
  failed,
  start,
  created,
  saved,
};

class S3ClovisWriter {
private:
  struct m0_uint128 id;

  std::shared_ptr<S3RequestObject> request;

  // Used to report to caller
  std::function<void()> handler_on_success;
  std::function<void()> handler_on_failed;

  S3ClovisWriterOpState state;
public:
  //struct m0_uint128 id;
  S3ClovisWriter(std::shared_ptr<S3RequestObject> req);

  S3ClovisWriterOpState get_state() {
    return state;
  }

  void advance_state();
  void mark_failed();

  // async create
  void create_object(std::function<void(void)> on_success, std::function<void(void)> on_failed);
  void create_object_successful();
  void create_object_failed();

  // Async save operation.
  void write_content(std::function<void(void)> on_success, std::function<void(void)> on_failed);
  void write_content_successful();
  void write_content_failed();

  // xxx remove this
  void set_up_clovis_data_buffers(struct s3_clovis_rw_op_context &ctx);
};

#endif
