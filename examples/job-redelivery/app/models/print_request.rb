class PrintRequest < ActiveRecord::Base
  def claim_submission
    self.class.with_connection do |connection|
      if connection.transaction_open?
        raise ArgumentError, "Print submission requires an autocommitted claim"
      end

      self.class.where(id: id, status: "pending").update_all(status: "unconfirmed") == 1
    end
  end
end
