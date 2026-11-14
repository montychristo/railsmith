class PrintDocumentJob < ActiveJob::Base
  def perform(request_id)
    request = PrintRequest.find_by(id: request_id)
    return unless request&.claim_submission

    receipt = Printer.submit(request.document_id)
    request.update!(status: "submitted", provider_receipt: receipt)
  end
end
