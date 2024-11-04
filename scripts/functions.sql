CREATE OR REPLACE FUNCTION get_queue_size()
RETURNS BIGINT SECURITY DEFINER AS $$
DECLARE
    max_messages_id BIGINT;
    max_transformed_id BIGINT;
    id_difference BIGINT;
BEGIN
    -- Get the highest 'id' from the 'messages' table
    SELECT COALESCE(MAX(id), 0) INTO max_messages_id FROM messages;

    -- Get the highest 'original_message_id' from the 'transformed_messages' table
    SELECT COALESCE(MAX(original_message_id), 0) INTO max_transformed_id 
    FROM transformed_messages;

    -- Calculate the difference
    id_difference := max_messages_id - max_transformed_id;

    -- Return the result
    RETURN id_difference;
END;
$$ LANGUAGE plpgsql; 
